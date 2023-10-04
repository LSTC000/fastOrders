from .schemas import CourierGetSchema, CourierGetAllSchema, CourierAddSchema
from .services import CourierDBService
from .dependencies import courier_db_service
from .details import CourierDetails

from app.common import config, Logger
from app.utils.response import BaseAPIResponse, StatusType

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix='/courier', tags=['Courier'])

logger = Logger(name=__name__, log_path=config.courier_log_path).get_logger()


@router.get('/{courier_id}', response_model=BaseAPIResponse)
async def get_courier(courier_id: int, db_service: CourierDBService = Depends(courier_db_service)):
    """
    courier_id: ID курьера, данные по которому вы хотите получить.

    В качестве ответа возвращается JSON объект в формате BaseAPIResponse: { 'status': str, 'data': {}, 'detail': str },
    с статусом 'success', если запрос был корректно выполнен и статусом 'error', если в процессе выполения звапроса
    возникла ошибка на стороне сервера. В обоих случаях код ответа: 200. Данные о курьере хранятся внутри ключа 'data'.

    При возникновении ошибки валидации входных данных на стороне пользователя вызывается Validation Error с кодом 422 и
    JSON объект { 'detail': [] } c подробной информацией об ошибке в ключе 'detail'.
    """

    response = BaseAPIResponse()

    try:
        # Получаем данные о курьере.
        courier_data = await db_service.get_courier(courier_id)

        # Проверям валидны ли полученные данные.
        if courier_data is not None:
            # В случае успеха отправляем их пользователю.
            response.data = {'courier_data': CourierGetSchema(**courier_data)}
        else:
            # В случае ошибки сообщаем пользователю, что запрашиваемый им курьер не найден.
            response.status = StatusType.error
            response.detail = CourierDetails.get_courier_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        # Если возникла непредвиденная ошибка, то отправляем пользователю ответ,
        # что данная проблема обнаружена и записываем её в соответствующий лог файл.
        response.status = StatusType.error
        response.detail = CourierDetails.exception_error
        logger.error(exc)
    finally:
        return response


@router.get('/', response_model=BaseAPIResponse)
async def get_couriers(db_service: CourierDBService = Depends(courier_db_service)):
    """
    В качестве ответа возвращается JSON объект в формате BaseAPIResponse: { 'status': str, 'data': {}, 'detail': str },
    с статусом 'success', если запрос был корректно выполнен и статусом 'error', если в процессе выполения звапроса
    возникла ошибка на стороне сервера. В обоих случаях код ответа: 200. Данные о курьерах хранятся внутри ключа 'data'.
    """

    response = BaseAPIResponse()

    try:
        # Получаем данные о курьере.
        couriers_data = await db_service.get_couriers()

        # Проверям валидны ли полученные данные.
        if couriers_data is not None:
            # В случае успеха отправляем их пользователю.
            response.data = {
                'couriers_data': [CourierGetAllSchema(**courier_data) for courier_data in couriers_data]
            }
        else:
            # В случае ошибки сообщаем пользователю, что в данный момент не существует ни одного курьера.
            response.status = StatusType.error
            response.detail = CourierDetails.get_couriers_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        # Если возникла непредвиденная ошибка, то отправляем пользователю ответ,
        # что данная проблема обнаружена и записываем её в соответствующий лог файл.
        response.status = StatusType.error
        response.detail = CourierDetails.exception_error
        logger.error(exc)
    finally:
        return response


@router.post('/', response_model=BaseAPIResponse)
async def add_courier(courier_data: CourierAddSchema, db_service: CourierDBService = Depends(courier_db_service)):
    """
    В качестве ответа возвращается JSON объект в формате BaseAPIResponse: { 'status': str, 'data': {}, 'detail': str },
    с статусом 'success', если запрос был корректно выполнен и статусом 'error', если в процессе выполения звапроса
    возникла ошибка на стороне сервера. В обоих случаях код ответа: 200. ID созданного курьера хранится
    внутри ключа 'data'.

    При возникновении ошибки валидации входных данных на стороне пользователя вызывается Validation Error с кодом 422 и
    JSON объект { 'detail': [] } c подробной информацией об ошибке в ключе 'detail'.
    """

    response = BaseAPIResponse()

    try:
        # Получаем id курьера в случае его успешного создания.
        courier_id = await db_service.add_courier(courier_data)

        # Проверям валидны ли полученные данные.
        if courier_id is not None:
            # В случае успеха добавляем все районы курьера в промежуточную таблицу couriers_districts.
            # Если в процессе добавления районов для курьера не возникнет ошибки IntegrityError, то
            # отправляем пользователю ID созданного курьера.
            try:
                await db_service.add_courier_districts(
                    courier_id=courier_id,
                    districts=courier_data.districts
                )

                response.data = {'courier_id': courier_id}
            except IntegrityError:
                # В случае ошибки добавления несуществующего района, отправляем пользователю сообщение, что при
                # создании курьера один из указанных им районов не существует.
                # Далее удаляем уже созданного курьера.
                response.status = StatusType.error
                response.detail = CourierDetails.district_does_not_exist
                await db_service.delete_courier(courier_id)
        else:
            # В случае ошибки сообщаем пользователю, чтобы он повторил попытку добавления нового курьера позже.
            response.status = StatusType.error
            response.detail = CourierDetails.add_courier_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        # Если возникла непредвиденная ошибка, то отправляем пользователю ответ,
        # что данная проблема обнаружена и записываем её в соответствующий лог файл.
        response.status = StatusType.error
        response.detail = CourierDetails.exception_error
        logger.error(exc)
    finally:
        return response
