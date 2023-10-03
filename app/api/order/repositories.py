from .models import Order

from app.api.courier.models import CourierDistrict, Courier

from app.utils.repositories import SQLAlchemyRepository


class OrderRepository(SQLAlchemyRepository):
    model = Order


class CourierRepository(SQLAlchemyRepository):
    model = Courier


class CourierDistrictRepository(SQLAlchemyRepository):
    model = CourierDistrict
