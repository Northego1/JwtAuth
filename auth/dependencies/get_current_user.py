from fastapi import (
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from auth.config import settings
from auth.dependencies.db import get_db_session
from auth.dependencies.jwt_getters import (
    get_access_jwt_from_headers,
    get_refresh_jwt_from_cookie
)
from auth.exceptions import AuthError
from auth.model import User
from auth.services.user_control import UserOperations
from auth.utils.jwt_utils import decode_jwt


class CurrentUser:
    def __init__(self, token: str, token_type: str):
        self.token_ = token
        self.token_type_ = token_type
        self.payload = None
        self.user: User = None

    def verify_token_and_decode_to_payload(self) -> None:
        try:
            self.payload = decode_jwt(self.token_)
            if self.payload.get('type') != self.token_type_:
                raise AuthError()
        except Exception as e:
            raise AuthError() from e

    async def get_current_user(self, session: AsyncSession) -> User:
        self.verify_token_and_decode_to_payload()
        try:
            self.user = await UserOperations.get_user(
                searching_parameter='id',
                value=self.payload.get('user_id'),
                session=session
            )
        except Exception as e:
            raise AuthError() from e
        return self.user


async def get_user_by_access_jwt(
    session: AsyncSession = Depends(get_db_session),
    token: str | None = Depends(get_access_jwt_from_headers)
) -> User | None:
    if not token:
        return None
    try:
        user = CurrentUser(token, settings.jwt.access_type)
        return await user.get_current_user(session)
    except AuthError:
        return None


async def get_user_by_refresh_jwt(
    session: AsyncSession = Depends(get_db_session),
    token: str | None = Depends(get_refresh_jwt_from_cookie)
) -> User | None:
    if not token:
        return None
    try:
        user = CurrentUser(token, settings.jwt.refresh_type)
        return await user.get_current_user(session)
    except AuthError:
        return None

