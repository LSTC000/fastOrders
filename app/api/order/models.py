from datetime import datetime
from typing import TYPE_CHECKING

from app.db import Base

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from app.api.post.models import Post


class Order(Base):
    __tablename__ = 'order'

    name: Mapped[str] = mapped_column(String(32), nullable=False)
