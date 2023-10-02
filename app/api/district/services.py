from .schemas import DistrictAddSchema

from app.utils.repositories import AbstractRepository
from app.utils.email import Email, EmailSchema, EmailMessages
from app.utils.celery import send_log_task


class DistrictDBService:
    def __init__(self, district_repository: type[AbstractRepository]):
        self.district_repository = district_repository()

    async def add_district(self, district_data: DistrictAddSchema) -> int | None:
        return await self.district_repository.add_one(district_data.model_dump())

    async def get_district(self, district_id: int) -> dict | None:
        return await self.district_repository.get_one(district_id)

    async def get_districts(self) -> dict | None:
        return await self.district_repository.get_all()


class DistrictEmailService:
    @staticmethod
    @send_log_task.task
    def send_error_log(error_log: str) -> None:
        email_schema = EmailSchema()

        Email.send_email(
            email_schema=email_schema,
            message=EmailMessages.error_log_message(subject='DISTRICT ERROR LOG', error_log=error_log)
        )
