from .schemas import OrderGetSchema, OrderAddSchema
from .services import OrderDBService, CourierDistrictDBService
from .dependencies import order_db_service, courier_district_db_service
from .details import OrderDetails

from app.common import config, Logger
from app.utils.response import BaseAPIResponse, StatusType

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix='/order', tags=['Order'])

logger = Logger(name=__name__, log_path=config.order_log_path).get_logger()


# @router.get('/{user_id}', response_model=BaseAPIResponse)
# async def get_user(
#         user_id: int,
#         db_service: UserDBService = Depends(user_db_service),
#         email_service: UserEmailService = Depends(user_email_service)
# ):
#     response = BaseAPIResponse()
#     try:
#         user_data = await db_service.get_user(user_id)
#
#         if user_data is not None:
#             response.data = {'user_data': UserSchema(**user_data)}
#         else:
#             response.status = StatusType.error
#             response.detail = UserDetails.get_user_error
#     except HTTPException as exc:
#         response.status = StatusType.error
#         response.detail = exc.detail
#     except Exception as exc:
#         response.status = StatusType.error
#         response.detail = UserDetails.exception_error
#         logger.error(exc)
#         email_service.send_error_log(str(exc))
#     finally:
#         return response
#
#
# @router.get('/posts/{user_id}', response_model=BaseAPIResponse)
# async def get_user_posts(
#         user_id: int,
#         db_service: UserDBService = Depends(user_db_service),
#         email_service: UserEmailService = Depends(user_email_service)
# ):
#     response = BaseAPIResponse()
#     try:
#         user_data = await db_service.get_user(user_id, posts_data=True)
#
#         if user_data is not None:
#             response.data = {
#                 'posts_data': [PostSchema(**post.__dict__) for post in user_data['posts']]
#             }
#         else:
#             response.status = StatusType.error
#             response.detail = UserDetails.get_user_error
#     except HTTPException as exc:
#         response.status = StatusType.error
#         response.detail = exc.detail
#     except Exception as exc:
#         response.status = StatusType.error
#         response.detail = UserDetails.exception_error
#         logger.error(exc)
#         email_service.send_error_log(str(exc))
#     finally:
#         return response
#
#
# @router.post('/', response_model=BaseAPIResponse)
# async def add_user(
#         user_data: UserAddSchema,
#         db_service: UserDBService = Depends(user_db_service),
#         email_service: UserEmailService = Depends(user_email_service)
# ):
#     response = BaseAPIResponse()
#     try:
#         user_id = await db_service.add_user(user_data)
#
#         if user_id is not None:
#             response.data = {'user_id': user_id}
#         else:
#             response.status = StatusType.error
#             response.detail = UserDetails.add_user_error
#     except IntegrityError:
#         response.status = StatusType.error
#         response.detail = UserDetails.email_exist
#     except HTTPException as exc:
#         response.status = StatusType.error
#         response.detail = exc.detail
#     except Exception as exc:
#         response.status = StatusType.error
#         response.detail = UserDetails.exception_error
#         logger.error(exc)
#         email_service.send_error_log(str(exc))
#     finally:
#         return response
