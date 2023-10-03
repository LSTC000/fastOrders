from .repositories import OrderRepository, CourierDistrictRepository
from .services import OrderDBService, CourierDistrictDBService


def order_db_service():
    return OrderDBService(OrderRepository)


def courier_district_db_service():
    return CourierDistrictDBService(CourierDistrictRepository)
