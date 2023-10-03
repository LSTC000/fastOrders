from typing import TYPE_CHECKING

from app.db import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from app.api.courier.models import Courier
    from app.api.order.models import Order


class District(Base):
    __tablename__ = 'district'

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    couriers: Mapped['Courier'] = relationship(secondary='courier_district', back_populates='districts')
    order: Mapped['Order'] = relationship(back_populates='district')
