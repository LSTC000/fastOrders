from pydantic import BaseModel


class DistrictGetSchema(BaseModel):
    id: int
    name: str


class DistrictAddSchema(BaseModel):
    name: str
