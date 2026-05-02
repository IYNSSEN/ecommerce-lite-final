import re
from app.repositories.user_repository import UserRepository
from app.utils.errors import ValidationError, ConflictError, UnauthorizedError
from app.utils.jwt_utils import create_token


class AuthService:
    def __init__(self):
        self.users = UserRepository()

    def register(self, data):
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""
        role = data.get("role") or "user"

        errors = []
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            errors.append({"field": "email", "message": "Valid email is required"})
        if len(password) < 6:
            errors.append({"field": "password", "message": "Password must be at least 6 characters"})
        if role not in ["user", "admin"]:
            errors.append({"field": "role", "message": "Role must be user or admin"})

        if errors:
            raise ValidationError(details=errors)

        if self.users.find_by_email(email):
            raise ConflictError("Email is already registered")

        user = self.users.create(email, password, role)
        return {"user": user.to_dict(), "token": create_token(user)}

    def login(self, data):
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        user = self.users.find_by_email(email)
        if not user or not user.check_password(password):
            raise UnauthorizedError("Invalid email or password")

        return {"user": user.to_dict(), "token": create_token(user)}
