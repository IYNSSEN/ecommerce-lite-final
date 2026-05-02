from datetime import datetime, timedelta, timezone
from functools import wraps
import jwt
from flask import current_app, request, g
from app.models import User
from app.utils.errors import UnauthorizedError, ForbiddenError


def create_token(user):
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=8)
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            raise UnauthorizedError("Missing Bearer token")

        token = auth.replace("Bearer ", "", 1).strip()
        try:
            payload = jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError("Token expired")
        except jwt.InvalidTokenError:
            raise UnauthorizedError("Invalid token")

        user = User.query.get(int(payload["sub"]))
        if not user:
            raise UnauthorizedError("User does not exist")

        g.current_user = user
        return fn(*args, **kwargs)
    return wrapper


def require_role(role):
    def decorator(fn):
        @wraps(fn)
        @require_auth
        def wrapper(*args, **kwargs):
            if g.current_user.role != role:
                raise ForbiddenError(f"Role '{role}' is required")
            return fn(*args, **kwargs)
        return wrapper
    return decorator
