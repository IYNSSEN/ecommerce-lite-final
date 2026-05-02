import json
import time
import uuid
from flask import request, g


def register_logging(app):
    @app.before_request
    def before_request():
        g.request_id = str(uuid.uuid4())
        g.start_time = time.time()

    @app.after_request
    def after_request(response):
        latency_ms = int((time.time() - g.get("start_time", time.time())) * 1000)
        log = {
            "level": "info",
            "msg": "request",
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "latencyMs": latency_ms,
            "requestId": g.get("request_id")
        }
        app.logger.info(json.dumps(log))
        response.headers["X-Request-Id"] = g.get("request_id", "")
        return response
