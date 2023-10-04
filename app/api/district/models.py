from typing import TYPE_CHECKING

from app.db import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from app.api.courier.models import Courier
    from app.api.order.models import Order


class District(Base):
    __tablename__ = 'district'

    # Уникальное название района.
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    # Связь с моделью Courier через промежуточную модель CourierDistrict.
    couriers: Mapped['Courier'] = relationship(secondary='courier_district', back_populates='districts')
    # Связь с моделью Order.
    order: Mapped['Order'] = relationship(back_populates='district')
