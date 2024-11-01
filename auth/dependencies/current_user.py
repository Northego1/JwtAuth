from httpx import request
import jwt
from auth.config import settings
from auth.service import get_user
from auth.utils.jwt_utils import decode_jwt
from auth.exceptions import AuthError
from auth.model import User
from auth.repository import DbUserOperations

from fastapi.security import HTTPBearer
from jwt.exceptions import InvalidTokenError
from fastapi.security import (
    HTTPAuthorizationCredentials,
)
from fastapi import (
    Depends,
    Request
)


# http_bearer = HTTPBearer()
# # oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/jwt/login')

# def get_user_access_payload(
#         credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
#         # token: str = Depends(oauth2_scheme)
# ):
#     token = credentials.credentials
#     payload= decode_jwt(token)
#     return payload


# def get_user_refresh_payload(
#         request: Request
# ):
#     token = request.cookies.get('refresh_jwt')
#     payload= decode_jwt(token)
#     return {
#         "token": token,
#         "payload": payload
#     }


# def get_current_user_from_token(token_type: str, payload: dict) -> User:
#     jwt_type = payload.get(settings.jwt.type_field)
#     if jwt_type != token_type:
#         raise AuthError(
#             detail=
#             f'По данному URL невозможно использовать {jwt_type!r} токен'
#             f'используйте {settings.jwt.access_type!r} токен'
#         )
#     username = payload.get('sub')
#     user: User = DbUserOperations.get_user(username)
#     if not user:
#         raise AuthError(detail='Пользователь не найден')
#     return user


# def get_current_user_for_refresh(
#         payload: dict = Depends(get_user_refresh_payload),
# ) -> User:  
#     user: User = get_current_user_from_token(
#         settings.jwt.refresh_type, payload)
#     return user


# def get_current_user(
#         payload: dict = Depends(get_user_access_payload),
# ) -> User:  
#     user: User = get_current_user_from_token(
#         settings.jwt.access_type, payload)
#     return user
    



def get_user_by_access_jwt(
        request: Request
):
    return JwtUserDependency(request, settings.jwt.access_type)


def get_user_by_refresh_jwt(
        request: Request
):
    return JwtUserDependency(request, settings.jwt.refresh_type)


class JwtUserDependency:
    def __init__(self, request: Request, token_type: str):
        self.token_type = token_type
        if self.token_type == settings.jwt.refresh_type:
            self.token = request.cookies.get('refresh_jwt')
        elif self.token_type == settings.jwt.access_type:
            self.token = request.headers.get('Authorization')


    def verify_and_decode_token(self):
        self.payload = decode_jwt(self.token)
        if self.payload.get('type') != self.token_type:
            raise AuthError()
        
    
    def get_current_user(self):
        user: User = get_user(self.payload.get('user_id'))
        return user