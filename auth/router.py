from fastapi import (
    APIRouter,
    Depends,
    Response
)
from auth.config import settings
from auth.dependencies.get_current_user import (
    get_user_by_access_jwt,
    get_user_by_refresh_jwt
)
from auth.dependencies.db import get_db_session
from auth.exceptions import AuthError
from auth.dependencies.fingerprint_handler import check_finger_print_jwt
from auth.services.user_control import (
    user_registration
)
from auth.utils.finger_print_utils import get_finger_print_hash
from auth.dependencies.jwt_create_manager import (
    create_access_token,
    create_refresh_token
)
from auth.model import User
from auth.pydantic_schemas.auth_responses import (
    AuthResponse200,
    AuthResponse40x,
    TokenInfo,
    ValidationResponse422
)

from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies.verify_user import verify_user


router = APIRouter(tags=['Auth'], prefix='/auth/jwt')



@router.post(
        '/login',
        response_model_exclude_none=True,
        responses={
            200: {"model": AuthResponse200},
            401: {"model": AuthResponse40x},
            403: {"model": AuthResponse40x},
            422: {"model": ValidationResponse422}
        },
)
async def auth_login(
    response: Response,
    user: User = Depends(verify_user),
    finger_print_hash: str = Depends(get_finger_print_hash),
    session: AsyncSession = Depends(get_db_session)
) -> AuthResponse200:
    
    access_jwt: str = create_access_token(user)
    refresh_jwt: str = await create_refresh_token(
        user=user,
        finger_print_hash=finger_print_hash,
        session=session
    )

    response.set_cookie(
        key="refresh_jwt",
        value=refresh_jwt,
        httponly=True,
        samesite='strict',
        max_age=(settings.jwt.refresh_expire * 60)
    )
    token = TokenInfo(access_token=access_jwt)
    return AuthResponse200(
        response_status=200,
        token=token.model_dump(exclude_none=True)
    )


@router.post(
        '/refresh',
        response_model_exclude_none=True,
        responses={
            200: {"model": AuthResponse200},
            401: {"model": AuthResponse40x},
            403: {"model": AuthResponse40x},
            422: {"model": ValidationResponse422}
        },
)
async def auth_refresh_jwt(
    user: User = Depends(get_user_by_refresh_jwt),
    valid_fingerprint: bool = Depends(check_finger_print_jwt)
) -> AuthResponse200:
    if not valid_fingerprint:
        raise AuthError()

    
    access_jwt = create_access_token(user)
    token = TokenInfo(
        access_token=access_jwt,
    )
    return AuthResponse200(
        response_status=200,
        token=token.model_dump(exclude_none=True)
    )


@router.get('/me')
def check_self_info(
    user: User = Depends(get_user_by_access_jwt)
):
    return {
        "username": user.username,
    }


@router.post(
        '/register',
        response_model_exclude_none=True,
        responses={
            200: {"model": AuthResponse200},
            400: {"model": AuthResponse40x},
        },
)
async def register_user(
    user: User = Depends(user_registration)
):
    return AuthResponse200(
        response_status=200,
        detail=f"user {user.id!r} succesfully registred"
    ).model_dump(exclude_none=True)