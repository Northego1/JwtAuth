from contextlib import asynccontextmanager
from functools import wraps

from fastapi import Depends, Request
from auth.dependencies.db import get_db_session
from auth.dependencies.jwt_getters import get_access_jwt_from_headers
from auth.exceptions import AuthError
from auth.utils.jwt_utils import decode_and_verify_jwt
from auth.db_repository.black_list_access_CRUD import BlackListCrud
from sqlalchemy.ext.asyncio import AsyncSession


def is_access_jwt_blacklisted(func: callable):
    @wraps(func)
    async def wrapper(
            request: Request = Depends(),
            *args,
            **kwargs
        ):
            session: AsyncSession = get_db_session()
            access_token: str = await get_access_jwt_from_headers(request=request)
            access_payload: dict = decode_and_verify_jwt(token=access_token)
            jti = access_payload.get('jti')
            
            async for session in get_db_session():
                if await BlackListCrud.read_access_token(
                    session=session,
                    jti=jti
                ):
                    raise AuthError(detail='Войдите в аккаунт')
            return await func(request, *args, **kwargs)
    return wrapper

