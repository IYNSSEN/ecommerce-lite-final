from time import time
from flask import request, jsonify

_login_attempts = {}


def register_security_headers(app):
    @app.after_request
    def add_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response


def register_rate_limit(app):
    @app.before_request
    def limit_login():
        if request.path != "/api/v1/auth/login" or request.method != "POST":
            return None

        ip = request.remote_addr or "unknown"
        now = time()
        window_seconds = 60
        max_attempts = 10

        attempts = [ts for ts in _login_attempts.get(ip, []) if now - ts < window_seconds]
        attempts.append(now)
        _login_attempts[ip] = attempts

        if len(attempts) > max_attempts:
            return jsonify({
                "error": {
                    "type": "RATE_LIMITED",
                    "message": "Too many login attempts. Try again later.",
                    "details": []
                }
            }), 429

        return None
