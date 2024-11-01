from auth.config import settings
from auth.utils.jwt_utils import decode_jwt
from auth.exceptions import AuthError
from auth.model import User
from auth.repository import db

from fastapi.security import HTTPBearer
from jwt.exceptions import InvalidTokenError
from fastapi.security import (
    HTTPAuthorizationCredentials,
)
from fastapi import (
    Depends
)


http_bearer = HTTPBearer()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/jwt/login')

def get_user_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
        # token: str = Depends(oauth2_scheme)
):
    token = credentials.credentials
    payload= decode_jwt(token)
    return payload


def get_current_user_from_token(token_type: str, payload: dict) -> User:
    jwt_type = payload.get(settings.jwt.type_field)
    if jwt_type != token_type:
        raise AuthError(
            detail=
            f'По данному URL невозможно использовать {jwt_type!r} токен'
            f'используйте {settings.jwt.access_type!r} токен'
        )
    username = payload.get('sub')
    user: User = db.get_user(username)
    if not user:
        raise AuthError(detail='Пользователь не найден')
    return user


def get_current_user_for_refresh(
        payload: dict = Depends(get_user_payload),
) -> User:  
    user: User = get_current_user_from_token(
        settings.jwt.refresh_type, payload)
    return user


def get_current_user(
        payload: dict = Depends(get_user_payload),
) -> User:  
    user: User = get_current_user_from_token(
        settings.jwt.access_type, payload)
    return user
    
    