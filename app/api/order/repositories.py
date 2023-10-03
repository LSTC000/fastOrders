from .models import Order

from app.api.courier.models import CourierDistrict

from app.utils.repositories import SQLAlchemyRepository


class OrderRepository(SQLAlchemyRepository):
    model = Order


class CourierDistrictRepository(SQLAlchemyRepository):
    model = CourierDistrict
