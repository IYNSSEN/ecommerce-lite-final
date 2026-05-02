from flask import Blueprint, jsonify
from sqlalchemy import text
from app.models import db

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@health_bp.get("/ready")
def ready():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "ready", "database": "ok"}), 200
    except Exception:
        return jsonify({"status": "not-ready", "database": "unavailable"}), 503
