from app.exceptions.app_exceptions import AppException


class UserNotFound(AppException):
    def __init__(self, user_id: int, status_code=404):
        super().__init__(
            f"User with ID {user_id} not found.", status_code
        )


class UsernameAlreadyExists(AppException):
    def __init__(self, message: str = "Username already exists"):
        super().__init__(message=message, status_code=409)


class EmailAlreadyExists(AppException):
    def __init__(self, message="Email already exists"):
        super().__init__(message=message, status_code=409)
