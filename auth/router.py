from fastapi import (
    APIRouter,
    Depends,
    Response
)
from fastapi.responses import HTMLResponse, JSONResponse
from auth.config import settings
from auth.dependencies.get_current_user import (
    get_user_by_access_jwt,
    get_user_by_refresh_jwt
)
from auth.dependencies.db import get_db_session
from auth.dependencies.jwt_getters import get_access_jwt_from_headers
from auth.exceptions import AuthError
from auth.dependencies.fingerprint_handler import check_finger_print_jwt
from auth.services.logout_control import LogoutControl
from auth.services.user_control import (
    user_registration
)
from auth.custom_middleware import is_access_jwt_blacklisted
from auth.utils.fingerprint_utils import get_fingerprint_hash
from auth.dependencies.jwt_create_manager import (
    create_access_token,
    create_refresh_token
)
from auth.models import User
from auth.pydantic_schemas.auth_responses import (
    AuthResponse200,
    AuthResponse40x,
    TokenInfo,
    ValidationResponse422
)

from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies.verify_user import verify_user
from auth.utils.jwt_utils import decode_and_verify_jwt


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
    finger_print_hash: str = Depends(get_fingerprint_hash),
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
        detail='success authorization',
        JWT=token.model_dump(exclude_none=True)
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
        raise AuthError(detail='invalid')

    
    access_jwt = create_access_token(user)

    token = TokenInfo(
        access_token=access_jwt,
    )
    return AuthResponse200(
            response_status=200,
            detail='success regisration',
            JWT=token.model_dump(exclude_none=True)
        )


@router.get('/me')
def check_self_info(
    user: User | None = Depends(get_user_by_access_jwt)
):
    if not user:
        return HTMLResponse(status_code=505)
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
        detail=f"user {user.username!r} succesfully registred"
    ).model_dump(exclude_none=True)


@router.post(
        '/logout',
        response_model_exclude_none=True,
        responses={
            200: {"model": AuthResponse200},
            400: {"model": AuthResponse40x},
        },
)
async def logout(
    access_token: str = Depends(get_access_jwt_from_headers),
    session: AsyncSession = Depends(get_db_session),
    fingerprint_hash: str = Depends(get_fingerprint_hash)
):
    access_jwt_payload: dict = decode_and_verify_jwt(token=access_token)
    
    logout_manager = LogoutControl(
        access_jwt_payload=access_jwt_payload,
        session=session,
    )
    await logout_manager.add_access_token_to_black_list(
        access_token=access_token
    )

    await logout_manager.revoke_refresh_token(
        fingerprint_hash=fingerprint_hash
    )

    return AuthResponse200(
        response_status=200,
        detail='success logout',
    )
    
# 1. создать блэк лист для аксес токенов и помещать туда при логауте на таймер
# времени жизни токена
# 2. реструктурировать приложение, создать прослойку между эндпоинтами и бизнес логикой
# чтобы можно было легко заменить бизнес логику на другую!!!