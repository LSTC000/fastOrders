from .repositories import DistrictRepository
from .services import DistrictDBService


def district_db_service():
    return DistrictDBService(DistrictRepository)
