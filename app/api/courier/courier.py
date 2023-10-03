from .schemas import CourierGetSchema, CourierGetAllSchema, CourierAddSchema, ActiveOrderSchema
from .services import CourierDBService
from .dependencies import courier_db_service
from .details import CourierDetails
from .utils import Utils

from app.common import config, Logger
from app.utils.response import BaseAPIResponse, StatusType

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix='/courier', tags=['Courier'])

logger = Logger(name=__name__, log_path=config.courier_log_path).get_logger()


@router.get('/{courier_id}', response_model=BaseAPIResponse)
async def get_courier(courier_id: int, db_service: CourierDBService = Depends(courier_db_service),):
    response = BaseAPIResponse()
    try:
        courier_data = await db_service.get_courier(courier_id)

        if courier_data is not None:
            active_order = await db_service.get_active_order(courier_id)
            response.data = {
                'courier_data': CourierGetSchema(
                    id=courier_id,
                    name=courier_data.get('name'),
                    active_order=ActiveOrderSchema(
                        order_id=active_order.get('id'),
                        order_name=active_order.get('name')
                    ) if active_order is not None else active_order,
                    avg_order_complete_time=Utils.avg_order_complete_time(
                        complete_time=courier_data.get('complete_time'),
                        complete_orders=courier_data.get('complete_orders')
                    ),
                    avg_day_orders=Utils.avg_day_orders(
                        complete_orders=courier_data.get('complete_orders'),
                        works_days=courier_data.get('works_days')
                    )
                )
            }
        else:
            response.status = StatusType.error
            response.detail = CourierDetails.get_courier_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        response.status = StatusType.error
        response.detail = CourierDetails.exception_error
        logger.error(exc)
    finally:
        return response


@router.get('/', response_model=BaseAPIResponse)
async def get_couriers(db_service: CourierDBService = Depends(courier_db_service)):
    response = BaseAPIResponse()
    try:
        couriers_data = await db_service.get_couriers()

        if couriers_data is not None:
            response.data = {
                'couriers_data': [CourierGetAllSchema(**courier_data) for courier_data in couriers_data]
            }
        else:
            response.status = StatusType.error
            response.detail = CourierDetails.get_couriers_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        response.status = StatusType.error
        response.detail = CourierDetails.exception_error
        logger.error(exc)
    finally:
        return response


@router.post('/', response_model=BaseAPIResponse)
async def add_courier(courier_data: CourierAddSchema, db_service: CourierDBService = Depends(courier_db_service)):
    response = BaseAPIResponse()
    try:
        courier_id = await db_service.add_courier(courier_data)

        if courier_id is not None:
            try:
                await db_service.add_courier_districts(
                    courier_id=courier_id,
                    districts=courier_data.districts
                )

                response.data = {'courier_id': courier_id}
            except IntegrityError:
                response.status = StatusType.error
                response.detail = CourierDetails.district_does_not_exist
                await db_service.delete_courier(courier_id)
        else:
            response.status = StatusType.error
            response.detail = CourierDetails.add_courier_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        response.status = StatusType.error
        response.detail = CourierDetails.exception_error
        logger.error(exc)
    finally:
        return response
