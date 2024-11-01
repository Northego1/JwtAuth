from fastapi import (
    APIRouter,
    Depends,
    Request,
    Response
)
from auth.utils.jwt_utils import create_access_token, create_refresh_token
from auth.model import User
from auth.pydantic_schemas.auth_responses import (
    AuthResponse200,
    AuthResponse40x,
    TokenInfo,
    ValidationResponse422
)
from auth.dependencies.current_user import (
    get_current_user,
    get_current_user_for_refresh
)
from auth.dependencies.validate_user import validate_user_auth


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
def auth_login(
    response: Response,
    user: User = Depends(validate_user_auth),
) -> AuthResponse200:

    refresh_jwt = create_refresh_token(user)
    access_jwt =  create_access_token(user)

    response.set_cookie(
        key="refresh_jwt",
        value=access_jwt,
        httponly=True,
        samesite=True
    )

    token = TokenInfo(
        access_token=access_jwt,
        refresh_token=refresh_jwt
    )
    return AuthResponse200(
        response_status=200,
        token=token.model_dump(exclude_none=True),
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
def auth_refresh_jwt(
    user: User = Depends(get_current_user_for_refresh)
) -> AuthResponse200:
    

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
    user: User = Depends(get_current_user)
):
    return {
        "username": user.username,
    }

