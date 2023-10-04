from datetime import datetime
from typing import TYPE_CHECKING

from app.db import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from app.api.order.models import Order
    from app.api.district.models import District


class Courier(Base):
    __tablename__ = 'courier'

    # Имя курьера.
    name: Mapped[str] = mapped_column(nullable=False)
    # Количество завершённых заказов.
    complete_orders: Mapped[int] = mapped_column(default=0)
    # Количество потраченных на доствки секунд.
    complete_time: Mapped[float] = mapped_column(default=0)
    # Количество рабочих дней.
    work_days: Mapped[int] = mapped_column(default=0)
    # Дата последнего выполненного заказа.
    last_finish_at: Mapped[datetime | None] = mapped_column(default=None)
    # Статус курьера: 0 - свободен, 1 - работает.
    status: Mapped[int] = mapped_column(default=0)
    # Связь с моделью Order.
    orders: Mapped['Order'] = relationship(back_populates='courier')
    # Связь с моделью District через промежуточную модель CourierDistrict.
    districts: Mapped['District'] = relationship(secondary='courier_district', back_populates='couriers')


class CourierDistrict(Base):
    __tablename__ = 'courier_district'

    # ID курьера.
    courier_id: Mapped[int] = mapped_column(ForeignKey('courier.id'), nullable=False)
    # ID района.
    district_id: Mapped[int] = mapped_column(ForeignKey('district.id'), nullable=False)
