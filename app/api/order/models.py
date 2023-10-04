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

    # Название заказа.
    name: Mapped[str] = mapped_column(nullable=False)
    # Статус заказа: 1 - в работе, 2 - доставлен.
    status: Mapped[int] = mapped_column(default=1)
    # ID курьера, выполняющего заказ.
    courier_id: Mapped[int] = mapped_column(ForeignKey('courier.id'), nullable=False)
    # ID района.
    district_id: Mapped[int] = mapped_column(ForeignKey('district.id'), nullable=False)
    # Дата начала выполнения заказа.
    start_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    # Дата окончания выполнения заказа.
    finish_at: Mapped[datetime | None] = mapped_column(default=None)
    # Связь с моделью Courier.
    courier: Mapped['Courier'] = relationship(back_populates='orders')
    # Связь с моделью District.
    district: Mapped['District'] = relationship(back_populates='order')
