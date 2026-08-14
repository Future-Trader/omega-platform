"""Authentication business logic."""

from sqlalchemy.orm import Session

from .exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from .repository import AuthRepository
from .security import (
    create_access_token,
    create_refresh_token,
)

from app.models.user import User


class AuthService:
    """Authentication application service."""

    def __init__(self, db: Session) -> None:
        self.repository = AuthRepository(db)

    def register(
        self,
        email: str,
        password_hash: str,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> User:
        existing = self.repository.get_by_email(email)

        if existing:
            raise UserAlreadyExistsError(
                "A user with this email already exists."
            )

        user = User(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
        )

        return self.repository.create(user)

    def authenticate(
        self,
        email: str,
        password_valid: bool,
    ) -> tuple[str, str]:
        user = self.repository.get_by_email(email)

        if user is None or not password_valid:
            raise InvalidCredentialsError(
                "Invalid email or password."
            )

        return (
            create_access_token(str(user.id)),
            create_refresh_token(str(user.id)),
        )
