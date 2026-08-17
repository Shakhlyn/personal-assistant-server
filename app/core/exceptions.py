from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.request_id import get_request_id


class ErrorCode:
    # --- generic ---
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"

    # --- auth ---
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"
    INVALID_TOKEN = "INVALID_TOKEN"
    INACTIVE_USER = "INACTIVE_USER"
    FORBIDDEN = "FORBIDDEN"

    # --- users ---
    USER_NOT_FOUND = "USER_NOT_FOUND"
    SELF_MODIFICATION_FORBIDDEN = "SELF_MODIFICATION_FORBIDDEN"

    # --- books ---
    TASK_NOT_FOUND = "TASK_NOT_FOUND"
    TASK_UNAVAILABLE = "TASK_UNAVAILABLE"


class AppException(Exception):
    def __init__(self, message: str, code: str, status_code: int = 400) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


# --------------------------------------------------------------------------
# auth
# --------------------------------------------------------------------------


class InvalidCredentials(AppException):
    """One error for both 'no such email' and 'wrong password'.

    Distinct messages turn the login endpoint into a user-enumeration oracle.
    """

    def __init__(self) -> None:
        super().__init__(
            message="Incorrect email or password",
            code=ErrorCode.INVALID_CREDENTIALS,
            status_code=401,
        )


class EmailAlreadyExists(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="An account with this email already exists",
            code=ErrorCode.EMAIL_ALREADY_EXISTS,
            status_code=409,
        )


class InvalidToken(AppException):
    def __init__(self, message: str = "Invalid or expired token") -> None:
        super().__init__(
            message=message,
            code=ErrorCode.INVALID_TOKEN,
            status_code=401,
        )


class InactiveUser(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="This account is disabled",
            code=ErrorCode.INACTIVE_USER,
            status_code=403,
        )


class Forbidden(AppException):
    def __init__(self, message: str = "Not enough permissions") -> None:
        super().__init__(
            message=message,
            code=ErrorCode.FORBIDDEN,
            status_code=403,
        )


# --------------------------------------------------------------------------
# users
# --------------------------------------------------------------------------


class UserNotFound(AppException):
    def __init__(self, user_id: int) -> None:
        super().__init__(
            message=f"User {user_id} not found",
            code=ErrorCode.USER_NOT_FOUND,
            status_code=404,
        )


class SelfModificationForbidden(AppException):
    """An admin demoting or disabling their own account can lock everyone out
    of admin permanently — there is no recovery path through the API."""

    def __init__(self) -> None:
        super().__init__(
            message="You cannot change your own role or disable your own account",
            code=ErrorCode.SELF_MODIFICATION_FORBIDDEN,
            status_code=403,
        )


# --------------------------------------------------------------------------
# tasks
# --------------------------------------------------------------------------


class TaskNotFound(AppException):
    def __init__(self, task_id: int) -> None:
        super().__init__(
            message=f"Task {task_id} not found",
            code=ErrorCode.TASK_NOT_FOUND,
            status_code=404,
        )


# --------------------------------------------------------------------------
#
# --------------------------------------------------------------------------




# --------------------------------------------------------------------------
# handler
# --------------------------------------------------------------------------


async def app_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, AppException)

    headers: dict[str, str] = {}
    # RFC 6750: a 401 from a bearer-protected resource must say so.
    if exc.status_code == 401:
        headers["WWW-Authenticate"] = "Bearer"

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "code": exc.code,
                "request_id": get_request_id(),
            }
        },
        headers=headers,
    )
