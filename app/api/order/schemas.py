from pydantic import BaseModel


class OrderGetSchema(BaseModel):
    courier_id: int
    status: int


class OrderAddSchema(BaseModel):
    name: str
    district: int
