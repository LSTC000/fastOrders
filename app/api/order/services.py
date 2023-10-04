from .schemas import OrderAddSchema
from .models import Order
from .repositories import Courier, CourierDistrict
from .utils import Utils

from app.utils.repositories import AbstractRepository


class OrderDBService:
    def __init__(
            self,
            order_repository: type[AbstractRepository],
            courier_repository: type[AbstractRepository],
            courier_district_repository: type[AbstractRepository]
    ):
        self.order_repository = order_repository()
        self.courier_repository = courier_repository()
        self.courier_district_repository = courier_district_repository()

    async def add_order(self, order_data: OrderAddSchema) -> tuple[int, int] | None:
        couriers = await self.__get_couriers(order_data.district)

        if couriers is not None:
            for courier in couriers:
                courier_data = await self.__check_courier(courier.get('courier_id'))
                if courier_data is not None:
                    courier_id = courier_data.get('id')

                    new_courier_data, new_order_data = Utils.start_order_new_data(
                        courier_data=courier_data,
                        order_data=order_data.model_dump()
                    )

                    order_id = await self.order_repository.add_one(new_order_data)

                    if order_id is None:
                        return order_id

                    await self.__edit_courier(
                        courier_id=courier_id,
                        new_courier_data=new_courier_data
                    )

                    return order_id, courier_id

        return None

    async def finish_order(self, order_id: int) -> int | None:
        order_data = await self.order_repository.get_one(
            target_id=order_id,
            query_expression=((Order.id == order_id) & (Order.status == 1))
        )

        if order_data is not None:
            courier_data = await self.courier_repository.get_one(order_data.get('courier_id'))

            new_courier_data, new_order_data = Utils.finish_order_new_data(
                courier_data=courier_data,
                order_data=order_data
            )

            await self.__edit_courier(
                courier_id=courier_data.get('id'),
                new_courier_data=new_courier_data
            )

            return await self.__edit_order(
                order_id=order_data.get('id'),
                new_order_data=new_order_data
            )

        return None

    async def get_order(self, order_id: int) -> dict | None:
        return await self.order_repository.get_one(order_id)

    async def __edit_courier(self, courier_id: int, new_courier_data) -> int | None:
        return await self.courier_repository.edit_one(
            target_id=courier_id,
            new_target_data=new_courier_data
        )

    async def __edit_order(self, order_id: int, new_order_data) -> int | None:
        return await self.order_repository.edit_one(
            target_id=order_id,
            new_target_data=new_order_data
        )

    async def __check_courier(self, courier_id: int) -> dict | None:
        return await self.courier_repository.get_one(
            target_id=courier_id,
            query_expression=((Courier.id == courier_id) & (Courier.status == 0))
        )

    async def __get_couriers(self, district_id: int) -> list[dict] | None:
        return await self.courier_district_repository.get_all(
            target_id=district_id,
            query_expression=(CourierDistrict.district_id == district_id)
        )
