from app.common import config

from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    smtp_user: EmailStr = config.smtp_user
    smtp_pass: str = config.smtp_pass
    smtp_host: str = config.smtp_host
    smtp_port: int = config.smtp_port
    sender: EmailStr = config.smtp_user
    getter: EmailStr | list[EmailStr] = config.smtp_user
