from .repositories import OrderRepository, CourierRepository, CourierDistrictRepository
from .services import OrderDBService


def order_db_service():
    return OrderDBService(
        order_repository=OrderRepository,
        courier_repository=CourierRepository,
        courier_district_repository=CourierDistrictRepository
    )
