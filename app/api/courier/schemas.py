from pydantic import BaseModel


class ActiveOrderSchema(BaseModel):
    order_id: int
    order_name: str


class CourierGetSchema(BaseModel):
    id: int
    name: str
    active_order: ActiveOrderSchema | None
    avg_order_complete_time: str
    avg_day_orders: int


class CourierGetAllSchema(BaseModel):
    id: int
    name: str


class CourierAddSchema(BaseModel):
    name: str
    districts: list[int]
