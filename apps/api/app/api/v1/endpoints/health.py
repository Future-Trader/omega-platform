from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.VERSION,
    }