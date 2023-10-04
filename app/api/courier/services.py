from .schemas import CourierAddSchema
from .repositories import Order
from .utils import Utils

from app.utils.repositories import AbstractRepository


class CourierDBService:
    def __init__(
            self,
            courier_repository: type[AbstractRepository],
            order_repository: type[AbstractRepository],
            courier_district_repository: type[AbstractRepository]
    ):
        self.courier_repository = courier_repository()
        self.order_repository = order_repository()
        self.courier_district_repository = courier_district_repository()

    async def add_courier(self, courier_data: CourierAddSchema) -> int | None:
        return await self.courier_repository.add_one({'name': courier_data.name})

    async def get_courier(self, courier_id: int) -> dict | None:
        courier_data = await self.courier_repository.get_one(courier_id)

        if courier_data is not None:
            active_order_data = await self.__get_active_order(courier_id)

            return Utils.get_courier_report(courier_data=courier_data, active_order_data=active_order_data)

        return None

    async def get_couriers(self) -> dict | None:
        return await self.courier_repository.get_all()

    async def delete_courier(self, courier_id: int) -> int | None:
        return await self.courier_repository.delete_one(courier_id)

    async def add_courier_districts(self, courier_id: int, districts: list[int]) -> list[int] | None:
        return await self.courier_district_repository.add_all(
            [{'courier_id': courier_id, 'district_id': district_id} for district_id in set(districts)]
        )

    async def __get_active_order(self, courier_id: int) -> dict | None:
        return await self.order_repository.get_one(
            target_id=courier_id,
            query_expression=((Order.courier_id == courier_id) & (Order.status == 1))
        )
