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

    name: Mapped[str] = mapped_column(nullable=False)
    complete_orders: Mapped[int] = mapped_column(default=0)
    complete_time: Mapped[float] = mapped_column(default=0)
    work_days: Mapped[int] = mapped_column(default=0)
    last_finish_at: Mapped[datetime | None] = mapped_column(default=None)
    status: Mapped[int] = mapped_column(default=0)
    orders: Mapped['Order'] = relationship(back_populates='courier')
    districts: Mapped['District'] = relationship(secondary='courier_district', back_populates='couriers')


class CourierDistrict(Base):
    __tablename__ = 'courier_district'

    courier_id: Mapped[int] = mapped_column(ForeignKey('courier.id'), nullable=False)
    district_id: Mapped[int] = mapped_column(ForeignKey('district.id'), nullable=False)
