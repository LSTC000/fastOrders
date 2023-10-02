from datetime import datetime
from typing import TYPE_CHECKING

from app.db import Base

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from app.api.order.models import Order


class Courier(Base):
    __tablename__ = 'courier'

    name: Mapped[str] = mapped_column(nullable=False)
    avg_order_complete_time: Mapped[datetime | None] = mapped_column()
    avg_day_orders: Mapped[int | None] = mapped_column()
    order: Mapped['Order'] = relationship(back_populates='courier')


class OrderStatus(Base):
    courier_id: Mapped[int] = mapped_column(ForeignKey('courier.id'), nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'), nullable=False)
