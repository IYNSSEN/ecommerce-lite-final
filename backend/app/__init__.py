import os
from flask import Flask, jsonify
from flask_cors import CORS
from .models import db
from .controllers.auth_controller import auth_bp
from .controllers.product_controller import product_bp
from .controllers.order_controller import order_bp
from .controllers.health_controller import health_bp
from .middleware.logging_middleware import register_logging
from .middleware.security_middleware import register_security_headers, register_rate_limit
from .utils.errors import ApiError


def create_app():
    app = Flask(__name__)

    database_url = os.getenv("DATABASE_URL", "sqlite:///ecommerce.db")
    if database_url.startswith("sqlite:///"):
        db_path = database_url.replace("sqlite:///", "")
        if not os.path.isabs(db_path):
            database_url = "sqlite:///" + os.path.join(os.getcwd(), db_path)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET"] = os.getenv("JWT_SECRET", "dev-secret-change-me")
    app.config["CORS_ORIGIN"] = os.getenv("CORS_ORIGIN", "*")

    CORS(app, origins=[app.config["CORS_ORIGIN"]] if app.config["CORS_ORIGIN"] != "*" else "*")
    db.init_app(app)

    register_logging(app)
    register_security_headers(app)
    register_rate_limit(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(product_bp, url_prefix="/api/v1/products")
    app.register_blueprint(order_bp, url_prefix="/api/v1")

    @app.errorhandler(ApiError)
    def handle_api_error(error):
        return jsonify({
            "error": {
                "type": error.code,
                "message": error.message,
                "details": error.details,
            }
        }), error.status_code

    @app.errorhandler(404)
    def handle_404(_):
        return jsonify({
            "error": {
                "type": "NOT_FOUND",
                "message": "The requested resource was not found",
                "details": []
            }
        }), 404

    @app.errorhandler(Exception)
    def handle_unexpected(error):
        app.logger.exception("Unexpected error")
        return jsonify({
            "error": {
                "type": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "details": []
            }
        }), 500

    with app.app_context():
        db.create_all()

    return app
