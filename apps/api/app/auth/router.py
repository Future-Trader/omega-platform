"""Authentication API endpoints."""

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
