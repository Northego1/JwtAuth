from httpx import request
import jwt
from auth.config import settings
from auth.services.user_control import UserOperations
from auth.utils.jwt_utils import decode_jwt
from auth.exceptions import AuthError
from auth.model import User

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer
from jwt.exceptions import InvalidTokenError
from fastapi.security import (
    HTTPAuthorizationCredentials,
)
from fastapi import (
    Depends,
    Request
)



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
        
    
    def get_current_user(self, session: AsyncSession):
        user: User = UserOperations.get_user(self.payload.get('user_id'))
        return userget_user