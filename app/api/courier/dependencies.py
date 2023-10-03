from .repositories import CourierRepository, CourierDistrictRepository, OrderRepository
from .services import CourierDBService


def courier_db_service():
    return CourierDBService(
        courier_repository=CourierRepository,
        order_repository=OrderRepository,
        courier_district_repository=CourierDistrictRepository
    )
