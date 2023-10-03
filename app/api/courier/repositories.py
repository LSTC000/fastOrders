from .models import Courier, CourierDistrict

from app.api.order.models import Order

from app.utils.repositories import SQLAlchemyRepository


class CourierRepository(SQLAlchemyRepository):
    model = Courier


class CourierDistrictRepository(SQLAlchemyRepository):
    model = CourierDistrict


class OrderRepository(SQLAlchemyRepository):
    model = Order
