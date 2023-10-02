from .repositories import DistrictRepository
from .services import DistrictDBService, DistrictEmailService


def district_db_service():
    return DistrictDBService(DistrictRepository)


def district_email_service():
    return DistrictEmailService
