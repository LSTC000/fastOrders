from .models import District

from app.utils.repositories import SQLAlchemyRepository


class DistrictRepository(SQLAlchemyRepository):
    model = District
