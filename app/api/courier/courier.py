from .schemas import UserSchema, UserAddSchema, UserEditSchema
from .services import UserDBService, UserEmailService
from .dependencies import user_db_service, user_email_service
from .details import UserDetails

from app.common import config, Logger
from app.utils.response import BaseAPIResponse, StatusType
from app.api.post.schemas import PostSchema

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix='/courier', tags=['Courier'])

logger = Logger(name=__name__, log_path=config.courier_log_path).get_logger()


@router.get('/{user_id}', response_model=BaseAPIResponse)
async def get_user(
        user_id: int,
        db_service: UserDBService = Depends(user_db_service),
        email_service: UserEmailService = Depends(user_email_service)
):
    response = BaseAPIResponse()
    try:
        user_data = await db_service.get_user(user_id)

        if user_data is not None:
            response.data = {'user_data': UserSchema(**user_data)}
        else:
            response.status = StatusType.error
            response.detail = UserDetails.get_user_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        response.status = StatusType.error
        response.detail = UserDetails.exception_error
        logger.error(exc)
        email_service.send_error_log(str(exc))
    finally:
        return response


@router.get('/posts/{user_id}', response_model=BaseAPIResponse)
async def get_user_posts(
        user_id: int,
        db_service: UserDBService = Depends(user_db_service),
        email_service: UserEmailService = Depends(user_email_service)
):
    response = BaseAPIResponse()
    try:
        user_data = await db_service.get_user(user_id, posts_data=True)

        if user_data is not None:
            response.data = {
                'posts_data': [PostSchema(**post.__dict__) for post in user_data['posts']]
            }
        else:
            response.status = StatusType.error
            response.detail = UserDetails.get_user_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        response.status = StatusType.error
        response.detail = UserDetails.exception_error
        logger.error(exc)
        email_service.send_error_log(str(exc))
    finally:
        return response


@router.post('/', response_model=BaseAPIResponse)
async def add_user(
        user_data: UserAddSchema,
        db_service: UserDBService = Depends(user_db_service),
        email_service: UserEmailService = Depends(user_email_service)
):
    response = BaseAPIResponse()
    try:
        user_id = await db_service.add_user(user_data)

        if user_id is not None:
            response.data = {'user_id': user_id}
        else:
            response.status = StatusType.error
            response.detail = UserDetails.add_user_error
    except IntegrityError:
        response.status = StatusType.error
        response.detail = UserDetails.email_exist
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        response.status = StatusType.error
        response.detail = UserDetails.exception_error
        logger.error(exc)
        email_service.send_error_log(str(exc))
    finally:
        return response


@router.patch('/', response_model=BaseAPIResponse)
async def edit_user(
        user_id: int,
        new_user_data: UserEditSchema,
        db_service: UserDBService = Depends(user_db_service),
        email_service: UserEmailService = Depends(user_email_service)
):
    response = BaseAPIResponse()
    try:
        user_id = await db_service.edit_user(user_id=user_id, new_user_data=new_user_data)

        if user_id is not None:
            response.data = {'user_id': user_id}
        else:
            response.status = StatusType.error
            response.detail = UserDetails.edit_user_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        response.status = StatusType.error
        response.detail = UserDetails.exception_error
        logger.error(exc)
        email_service.send_error_log(str(exc))
    finally:
        return response


@router.delete('/', response_model=BaseAPIResponse)
async def delete_user(
        user_id: int,
        db_service: UserDBService = Depends(user_db_service),
        email_service: UserEmailService = Depends(user_email_service)
):
    response = BaseAPIResponse()
    try:
        user_id = await db_service.delete_user(user_id)

        if user_id is not None:
            response.data = {'user_id': user_id}
        else:
            response.status = StatusType.error
            response.detail = UserDetails.delete_user_error
    except HTTPException as exc:
        response.status = StatusType.error
        response.detail = exc.detail
    except Exception as exc:
        response.status = StatusType.error
        response.detail = UserDetails.exception_error
        logger.error(exc)
        email_service.send_error_log(str(exc))
    finally:
        return response
