from .schemas import DistrictGetSchema, DistrictAddSchema
from .services import DistrictDBService
from .dependencies import district_db_service
from .details import DistrictDetails

from app.common import config, Logger
from app.utils.response import BaseAPIResponse, StatusType

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix='/district', tags=['District'])

logger = Logger(name=__name__, log_path=config.district_log_path).get_logger()


@router.get('/{district_id}', response_model=BaseAPIResponse)
async def get_district(district_id: int, db_service: DistrictDBService = Depends(district_db_service)):
    """
    district_id: ID района, данные по которому вы хотите получить.

    В качестве ответа возвращается JSON объект в формате BaseAPIResponse: { 'status': str, 'data': {}, 'detail': str },
    с статусом 'success', если запрос был корректно выполнен и статусом 'error', если в процессе выполения звапроса
    возникла ошибка на стороне сервера. В обоих случаях код ответа: 200. Данные о районе хранятся внутри ключа 'data'.

    При возникновении ошибки валидации входных данных на стороне пользователя вызывается Validation Error с кодом 422 и
    JSON объект { 'detail': [] } c подробной информацией об ошибке в ключе 'detail'.
    """

    response = BaseAPIResponse()

    try:
        # Получаем данные о районе.
        district_data = await db_service.get_district(district_id)

        # Проверям валидны ли полученные данные.
        if district_data is not None:
            # В случае успеха отправляем их пользователю.
            response.data = {'district_data': DistrictGetSchema(**district_data)}
        else:
            # В случае ошибки сообщаем пользователю, что запрашиваемый им район не найден.
            response.status = StatusType.error
            response.detail = DistrictDetails.get_district_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        # Если возникла непредвиденная ошибка, то отправляем пользователю ответ,
        # что данная проблема обнаружена и записываем её в соответствующий лог файл.
        response.status = StatusType.error
        response.detail = DistrictDetails.exception_error
        logger.error(exc)
    finally:
        return response


@router.get('/', response_model=BaseAPIResponse)
async def get_districts(db_service: DistrictDBService = Depends(district_db_service)):
    """
    В качестве ответа возвращается JSON объект в формате BaseAPIResponse: { 'status': str, 'data': {}, 'detail': str },
    с статусом 'success', если запрос был корректно выполнен и статусом 'error', если в процессе выполения звапроса
    возникла ошибка на стороне сервера. В обоих случаях код ответа: 200. Данные о районах хранятся внутри ключа 'data'.
    """

    response = BaseAPIResponse()

    try:
        # Получаем данные о районах.
        districts_data = await db_service.get_districts()

        # Проверям валидны ли полученные данные.
        if districts_data is not None:
            # В случае успеха отправляем их пользователю.
            response.data = {
                'districts_data': [DistrictGetSchema(**district_data) for district_data in districts_data]
            }
        else:
            # В случае ошибки сообщаем пользователю, что в данный момент не существует ни одного район.
            response.status = StatusType.error
            response.detail = DistrictDetails.get_districts_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        # Если возникла непредвиденная ошибка, то отправляем пользователю ответ,
        # что данная проблема обнаружена и записываем её в соответствующий лог файл.
        response.status = StatusType.error
        response.detail = DistrictDetails.exception_error
        logger.error(exc)
    finally:
        return response


@router.post('/', response_model=BaseAPIResponse)
async def add_district(district_data: DistrictAddSchema, db_service: DistrictDBService = Depends(district_db_service)):
    """
    В качестве ответа возвращается JSON объект в формате BaseAPIResponse: { 'status': str, 'data': {}, 'detail': str },
    с статусом 'success', если запрос был корректно выполнен и статусом 'error', если в процессе выполения звапроса
    возникла ошибка на стороне сервера. В обоих случаях код ответа: 200. ID созданного района хранится
    внутри ключа 'data'.

    При возникновении ошибки валидации входных данных на стороне пользователя вызывается Validation Error с кодом 422 и
    JSON объект { 'detail': [] } c подробной информацией об ошибке в ключе 'detail'.
    """

    response = BaseAPIResponse()

    try:
        # Получаем id района в случае его успешного добавления.
        district_id = await db_service.add_district(district_data)

        # Проверям валидны ли полученные данные.
        if district_id is not None:
            # В случае успеха id района пользователю.
            response.data = {'district_id': district_id}
        else:
            # В случае ошибки сообщаем пользователю, чтобы он повторил попытку добавления нового района позже.
            response.status = StatusType.error
            response.detail = DistrictDetails.add_district_error
    except IntegrityError:
        # В пользователь ввёл название района, которое уже есть в БД, то сообщаем ему об этом.
        response.status = StatusType.error
        response.detail = DistrictDetails.district_name_exist
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        # Если возникла непредвиденная ошибка, то отправляем пользователю ответ,
        # что данная проблема обнаружена и записываем её в соответствующий лог файл.
        response.status = StatusType.error
        response.detail = DistrictDetails.exception_error
        logger.error(exc)
    finally:
        return response
