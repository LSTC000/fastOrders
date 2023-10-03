from .schemas import DistrictAddSchema

from app.utils.repositories import AbstractRepository


class DistrictDBService:
    def __init__(self, district_repository: type[AbstractRepository]):
        self.district_repository = district_repository()

    async def add_district(self, district_data: DistrictAddSchema) -> int | None:
        return await self.district_repository.add_one(district_data.model_dump())

    async def get_district(self, district_id: int) -> dict | None:
        return await self.district_repository.get_one(district_id)

    async def get_districts(self) -> dict | None:
        return await self.district_repository.get_all()
