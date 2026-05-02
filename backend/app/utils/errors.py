class ApiError(Exception):
    def __init__(self, status_code, code, message, details=None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or []


class ValidationError(ApiError):
    def __init__(self, message="Validation failed", details=None):
        super().__init__(400, "VALIDATION_ERROR", message, details)


class UnauthorizedError(ApiError):
    def __init__(self, message="Authentication is required"):
        super().__init__(401, "UNAUTHORIZED", message, [])


class ForbiddenError(ApiError):
    def __init__(self, message="You do not have permission to perform this action"):
        super().__init__(403, "FORBIDDEN", message, [])


class NotFoundError(ApiError):
    def __init__(self, message="Resource not found"):
        super().__init__(404, "NOT_FOUND", message, [])


class ConflictError(ApiError):
    def __init__(self, message="Conflict"):
        super().__init__(409, "CONFLICT", message, [])


class ServiceUnavailableError(ApiError):
    def __init__(self, message="Dependency is unavailable"):
        super().__init__(503, "SERVICE_UNAVAILABLE", message, [])
