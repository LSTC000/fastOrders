from app.db import Base

from sqlalchemy.orm import Mapped, mapped_column


class District(Base):
    __tablename__ = 'district'

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
