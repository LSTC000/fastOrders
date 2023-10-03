from datetime import datetime
from typing import TYPE_CHECKING

from app.db import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from app.api.courier.models import Courier
    from app.api.district.models import District


class Order(Base):
    __tablename__ = 'order'

    name: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[int] = mapped_column(default=1)
    courier_id: Mapped[int] = mapped_column(ForeignKey('courier.id'), nullable=False)
    district_id: Mapped[int] = mapped_column(ForeignKey('district.id'), nullable=False)
    start_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    finish_at: Mapped[datetime | None] = mapped_column(default=None)
    courier: Mapped['Courier'] = relationship(back_populates='orders')
    district: Mapped['District'] = relationship(back_populates='order')
