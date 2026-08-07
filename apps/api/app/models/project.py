from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Project(BaseModel):
    __tablename__ = "projects"

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id")
    )

    name: Mapped[str] = mapped_column(String(255))

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )