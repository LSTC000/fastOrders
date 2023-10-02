from app.common import config

from celery import Celery


send_log_task = Celery(
    'send_log',
    broker=f'amqp://{config.rabbitmq_user}:{config.rabbitmq_pass}@{config.rabbitmq_host}:{config.rabbitmq_port}',
    backend=f'redis://{config.redis_host}:{config.redis_port}'
)
