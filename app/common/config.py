import os
from dataclasses import dataclass, field

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


@dataclass(frozen=True)
class Config:
    origins: list[str] = field(default_factory=lambda: os.getenv('ORIGINS', '').split(','))

    smtp_user: str = os.getenv('SMTP_USER')
    smtp_pass: str = os.getenv('SMTP_PASS')
    smtp_host: str = os.getenv('SMTP_HOST')
    smtp_port: int = os.getenv('SMTP_PORT')

    rabbitmq_user: str = os.getenv('RABBITMQ_USER')
    rabbitmq_pass: str = os.getenv('RABBITMQ_PASS')
    rabbitmq_host: str = os.getenv('RABBITMQ_HOST')
    rabbitmq_port: int = os.getenv('RABBITMQ_PORT')

    redis_host: str = os.getenv('REDIS_HOST')
    redis_port: int = os.getenv('REDIS_PORT')

    db_user: str = os.getenv('DB_USER')
    db_pass: str = os.getenv('DB_PASS')
    db_host: str = os.getenv('DB_HOST')
    db_port: int = os.getenv('DB_PORT')
    db_name: str = os.getenv('DB_NAME')

    courier_log_path: str = r'logs/courier.log'
    order_log_path: str = r'logs/order.log'
    district_log_path: str = r'logs/district.log'
