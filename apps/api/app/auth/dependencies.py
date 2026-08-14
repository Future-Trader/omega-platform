"""FastAPI authentication dependencies."""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db

from .exceptions import InvalidTokenError
from .repository import AuthRepository
from .security import decode_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = decode_token(token)

    if payload.get("type") != "access":
        raise InvalidTokenError(
            "Access token required."
        )

    subject = payload.get("sub")

    if not subject:
        raise InvalidTokenError(
            "Token subject is missing."
        )

    repository = AuthRepository(db)
    user = repository.get_by_id(int(subject))

    if user is None:
        raise InvalidTokenError(
            "Authenticated user was not found."
        )

    return user
