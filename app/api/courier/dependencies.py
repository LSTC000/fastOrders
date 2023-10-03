from .repositories import CourierRepository, CourierDistrictRepository, CourierOrderRepository
from .services import CourierDBService, CourierDistrictDBService, CourierOrderDBService


def courier_db_service():
    return CourierDBService(CourierRepository)


def courier_district_db_service():
    return CourierDistrictDBService(CourierDistrictRepository)


def courier_order_db_service():
    return CourierOrderDBService(CourierOrderRepository)
