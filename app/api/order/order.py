from .schemas import OrderGetSchema, OrderAddSchema
from .services import OrderDBService
from .dependencies import order_db_service
from .details import OrderDetails

from app.common import config, Logger
from app.utils.response import BaseAPIResponse, StatusType

from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(prefix='/order', tags=['Order'])

logger = Logger(name=__name__, log_path=config.order_log_path).get_logger()


@router.get('/{order_id}', response_model=BaseAPIResponse)
async def get_order(order_id: int, db_service: OrderDBService = Depends(order_db_service)):
    """
    order_id: ID заказа, данные по которому вы хотите получить.

    В качестве ответа возвращается JSON объект в формате BaseAPIResponse: { 'status': str, 'data': {}, 'detail': str },
    с статусом 'success', если запрос был корректно выполнен и статусом 'error', если в процессе выполения звапроса
    возникла ошибка на стороне сервера. В обоих случаях код ответа: 200. Данные о заказе хранятся внутри ключа 'data'.

    При возникновении ошибки валидации входных данных на стороне пользователя вызывается Validation Error с кодом 422 и
    JSON объект { 'detail': [] } c подробной информацией об ошибке в ключе 'detail'.
    """

    # Создаём объект ответа API.
    response = BaseAPIResponse()

    try:
        # Получаем данные о курьере.
        order_data = await db_service.get_order(order_id)

        # Проверям валидны ли полученные данные.
        if order_data is not None:
            # В случае успеха отправляем их пользователю.
            response.data = {'order_data': OrderGetSchema(**order_data)}
        else:
            # В случае ошибки сообщаем пользователю, что запрашиваемый им заказ не найден.
            response.status = StatusType.error
            response.detail = OrderDetails.get_order_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        # Если возникла непредвиденная ошибка, то отправляем пользователю ответ,
        # что данная проблема обнаружена и записываем её в соответствующий лог файл.
        response.status = StatusType.error
        response.detail = OrderDetails.exception_error
        logger.error(exc)
    finally:
        return response


@router.post('/', response_model=BaseAPIResponse)
async def add_order(order_data: OrderAddSchema, db_service: OrderDBService = Depends(order_db_service)):
    """
    В качестве ответа возвращается JSON объект в формате BaseAPIResponse: { 'status': str, 'data': {}, 'detail': str },
    с статусом 'success', если запрос был корректно выполнен и статусом 'error', если в процессе выполения звапроса
    возникла ошибка на стороне сервера. В обоих случаях код ответа: 200. ID созданного заказа хранится
    внутри ключа 'data'.

    При возникновении ошибки валидации входных данных на стороне пользователя вызывается Validation Error с кодом 422 и
    JSON объект { 'detail': [] } c подробной информацией об ошибке в ключе 'detail'.
    """

    # Создаём объект ответа API.
    response = BaseAPIResponse()

    try:
        # Получаем данные c id заказа и id курьера.
        data = await db_service.add_order(order_data)

        # Проверям валидны ли полученные данные.
        if data is not None:
            # В случае успеха отправляем id заказа и id курьера пользователю.
            response.data = {
                'order_id': data[0],
                'courier_id': data[1]
            }
        else:
            # В случае ошибки сообщаем пользователю, что в данный момент не удалось создать заказ по причине
            # отсутствия свободного курьера в указанном районе. Если пользователь введёт не валидный район, то
            # ошибка IntegrityError не будет вызвана, так как мы только ищем курьера с указанным районом,
            # а не добавляем его в courier_districts.
            response.status = StatusType.error
            response.detail = OrderDetails.add_order_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        # Если возникла непредвиденная ошибка, то отправляем пользователю ответ,
        # что данная проблема обнаружена и записываем её в соответствующий лог файл.
        response.status = StatusType.error
        response.detail = OrderDetails.exception_error
        logger.error(exc)
    finally:
        return response


@router.post('/{order_id}', response_model=BaseAPIResponse)
async def finish_order(order_id: int, db_service: OrderDBService = Depends(order_db_service)):
    """
    order_id: ID заказа, который вы хотите завершить.

    В качестве ответа возвращается JSON объект в формате BaseAPIResponse: { 'status': str, 'data': {}, 'detail': str },
    с статусом 'success', если запрос был корректно выполнен и статусом 'error', если в процессе выполения звапроса
    возникла ошибка на стороне сервера. В обоих случаях код ответа: 200. ID завершённого заказа хранится
    внутри ключа 'data'.

    При возникновении ошибки валидации входных данных на стороне пользователя вызывается Validation Error с кодом 422 и
    JSON объект { 'detail': [] } c подробной информацией об ошибке в ключе 'detail'.
    """

    # Создаём объект ответа API.
    response = BaseAPIResponse()

    try:
        # Получаем id заказа в случае его успешного завершения.
        order_id = await db_service.finish_order(order_id)

        # Проверям валиден ли полученный id.
        if order_id is not None:
            # В случае успеха отправляем его пользователю.
            response.data = {'order_id': order_id}
        else:
            # В случае ошибки сообщаем пользователю, что данный заказ не существует или он уже доставлен.
            response.status = StatusType.error
            response.detail = OrderDetails.finish_order_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        # Если возникла непредвиденная ошибка, то отправляем пользователю ответ,
        # что данная проблема обнаружена и записываем её в соответствующий лог файл.
        response.status = StatusType.error
        response.detail = OrderDetails.exception_error
        logger.error(exc)
    finally:
        return response
