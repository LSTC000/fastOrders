from .schemas import OrderGetSchema, OrderAddSchema
from .services import OrderDBService
from .dependencies import order_db_service
from .details import OrderDetails

from app.common import config, Logger
from app.utils.response import BaseAPIResponse, StatusType

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix='/order', tags=['Order'])

logger = Logger(name=__name__, log_path=config.order_log_path).get_logger()


@router.get('/{order_id}', response_model=BaseAPIResponse)
async def get_order(order_id: int, db_service: OrderDBService = Depends(order_db_service)):
    response = BaseAPIResponse()
    try:
        order_data = await db_service.get_order(order_id)

        if order_data is not None:
            response.data = {'order_data': OrderGetSchema(**order_data)}
        else:
            response.status = StatusType.error
            response.detail = OrderDetails.get_order_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        response.status = StatusType.error
        response.detail = OrderDetails.exception_error
        logger.error(exc)
    finally:
        return response


@router.post('/', response_model=BaseAPIResponse)
async def add_order(order_data: OrderAddSchema, db_service: OrderDBService = Depends(order_db_service)):
    response = BaseAPIResponse()
    try:
        data = await db_service.add_order(order_data)

        if data is not None:
            response.data = {
                'order_id': data[0],
                'courier_id': data[1]
            }
        else:
            response.status = StatusType.error
            response.detail = OrderDetails.add_order_error
    except IntegrityError:
        response.status = StatusType.error
        response.detail = OrderDetails.district_does_not_exist
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        response.status = StatusType.error
        response.detail = OrderDetails.exception_error
        logger.error(exc)
    finally:
        return response


@router.post('/{order_id}', response_model=BaseAPIResponse)
async def finish_order(order_id: int, db_service: OrderDBService = Depends(order_db_service)):
    response = BaseAPIResponse()
    try:
        order_id = await db_service.finish_order(order_id)

        if order_id is not None:
            response.data = {'order_id': order_id}
        else:
            response.status = StatusType.error
            response.detail = OrderDetails.finish_order_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        response.status = StatusType.error
        response.detail = OrderDetails.exception_error
        logger.error(exc)
    finally:
        return response
