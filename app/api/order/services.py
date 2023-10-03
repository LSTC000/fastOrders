from .schemas import OrderAddSchema

from app.utils.repositories import AbstractRepository


class OrderDBService:
    def __init__(self, courier_repository: type[AbstractRepository]):
        self.courier_repository = courier_repository()

    async def add_courier(self, courier_data: OrderAddSchema) -> int | None:
        return await self.courier_repository.add_one(courier_data.model_dump())

    async def get_courier(self, courier_id: int) -> dict | None:
        return await self.courier_repository.get_one(courier_id)

    async def get_couriers(self) -> dict | None:
        return await self.courier_repository.get_all()


class CourierDistrictDBService:
    def __init__(self, district_repository: type[AbstractRepository]):
        self.district_repository = district_repository()

    async def get_couriers(self, district_id: int) -> list[dict] | None:
        return await self.district_repository.get_all(district_id)
