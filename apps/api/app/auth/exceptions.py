"""Authentication exceptions."""


class AuthenticationError(Exception):
    """Base authentication exception."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when authentication credentials are invalid."""


class InvalidTokenError(AuthenticationError):
    """Raised when an authentication token is invalid."""


class UserAlreadyExistsError(AuthenticationError):
    """Raised when a user already exists."""
