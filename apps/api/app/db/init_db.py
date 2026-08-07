from app.db.base_class import Base
from app.db.session import engine

# Import models so SQLAlchemy registers them
from app.models.user import User  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)