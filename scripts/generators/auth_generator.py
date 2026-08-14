from __future__ import annotations

from pathlib import Path
from typing import Any


def _write_file(
    path: Path,
    content: str,
    overwrite: bool,
    dry_run: bool,
    created: list[str],
    modified: list[str],
    skipped: list[str],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    relative = str(path)

    if path.exists() and not overwrite:
        skipped.append(relative)
        return

    if path.exists():
        modified.append(relative)
    else:
        created.append(relative)

    if not dry_run:
        path.write_text(
            content,
            encoding="utf-8",
        )


def generate_auth(
    config: Any,
    **_: Any,
) -> dict[str, list[str]]:
    """Generate the OMEGA Authentication & Security foundation."""

    root = Path(config.root_directory)
    auth = root / "apps" / "api" / "app" / "auth"

    created: list[str] = []
    modified: list[str] = []
    skipped: list[str] = []
    errors: list[str] = []

    files: dict[str, str] = {
        "__init__.py": '''"""OMEGA authentication package."""\n''',

        "constants.py": '''"""Authentication constants for OMEGA."""


ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

TOKEN_TYPE = "bearer"
''',

        "exceptions.py": '''"""Authentication exceptions."""


class AuthenticationError(Exception):
    """Base authentication exception."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when authentication credentials are invalid."""


class InvalidTokenError(AuthenticationError):
    """Raised when an authentication token is invalid."""


class UserAlreadyExistsError(AuthenticationError):
    """Raised when a user already exists."""
''',

        "schemas.py": '''"""Authentication request and response schemas."""

from pydantic import BaseModel, ConfigDict, EmailStr


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
''',

        "security.py": '''"""Authentication security utilities."""

from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings

from .constants import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    TOKEN_TYPE,
)
from .exceptions import InvalidTokenError


def create_access_token(subject: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "type": "access",
        "exp": expires,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def create_refresh_token(subject: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = {
        "sub": subject,
        "type": "refresh",
        "exp": expires,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
    except jwt.PyJWTError as exc:
        raise InvalidTokenError(
            "Invalid or expired authentication token."
        ) from exc
''',

        "repository.py": '''"""Authentication data access layer."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class AuthRepository:
    """Database operations used by authentication."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(
            User.email == email
        )

        return self.db.scalar(statement)

    def get_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(
            User.id == user_id
        )

        return self.db.scalar(statement)

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
''',

        "service.py": '''"""Authentication business logic."""

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
''',

        "dependencies.py": '''"""FastAPI authentication dependencies."""

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
''',

        "router.py": '''"""Authentication API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from .dependencies import get_current_user
from .schemas import UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user=Depends(get_current_user),
):
    return current_user


@router.post("/logout")
def logout():
    return {
        "message": "Logout endpoint ready."
    }
''',
    }

    try:
        for filename, content in files.items():
            _write_file(
                auth / filename,
                content,
                config.overwrite,
                config.dry_run,
                created,
                modified,
                skipped,
            )

    except Exception as exc:
        errors.append(str(exc))

    return {
        "created": created,
        "modified": modified,
        "skipped": skipped,
        "errors": errors,
    }
