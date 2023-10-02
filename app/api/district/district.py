from .schemas import DistrictGetSchema, DistrictAddSchema
from .services import DistrictDBService, DistrictEmailService
from .dependencies import district_db_service, district_email_service
from .details import DistrictDetails

from app.common import config, Logger
from app.utils.response import BaseAPIResponse, StatusType

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix='/district', tags=['District'])

logger = Logger(name=__name__, log_path=config.district_log_path).get_logger()


@router.get('/{district_id}', response_model=BaseAPIResponse)
async def get_district(
        district_id: int,
        db_service: DistrictDBService = Depends(district_db_service),
        email_service: DistrictEmailService = Depends(district_email_service)
):
    response = BaseAPIResponse()
    try:
        district_data = await db_service.get_district(district_id)

        if district_data is not None:
            response.data = {'district_data': DistrictGetSchema(**district_data)}
        else:
            response.status = StatusType.error
            response.detail = DistrictDetails.get_district_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        response.status = StatusType.error
        response.detail = DistrictDetails.exception_error
        logger.error(exc)
        email_service.send_error_log(str(exc))
    finally:
        return response


@router.get('/', response_model=BaseAPIResponse)
async def get_districts(
        db_service: DistrictDBService = Depends(district_db_service),
        email_service: DistrictEmailService = Depends(district_email_service)
):
    response = BaseAPIResponse()
    try:
        districts_data = await db_service.get_districts()

        if districts_data is not None:
            response.data = {
                'districts_data': [DistrictGetSchema(**district_data) for district_data in districts_data]
            }
        else:
            response.status = StatusType.error
            response.detail = DistrictDetails.get_districts_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        response.status = StatusType.error
        response.detail = DistrictDetails.exception_error
        logger.error(exc)
        email_service.send_error_log(str(exc))
    finally:
        return response


@router.post('/', response_model=BaseAPIResponse)
async def add_district(
        district_data: DistrictAddSchema,
        db_service: DistrictDBService = Depends(district_db_service),
        email_service: DistrictEmailService = Depends(district_email_service)
):
    response = BaseAPIResponse()
    try:
        district_id = await db_service.add_district(district_data)

        if district_id is not None:
            response.data = {'district_id': district_id}
        else:
            response.status = StatusType.error
            response.detail = DistrictDetails.add_district_error
    except IntegrityError:
        response.status = StatusType.error
        response.detail = DistrictDetails.district_name_exist
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        response.status = StatusType.error
        response.detail = DistrictDetails.exception_error
        logger.error(exc)
        email_service.send_error_log(str(exc))
    finally:
        return response
