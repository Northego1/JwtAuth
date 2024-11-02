from auth.dependencies.db import get_db_session
from auth.utils.password_utils import check_password
from auth.exceptions import AuthError
from auth.model import User
from auth.db_repository.users import UserOperations

from sqlalchemy.ext.asyncio import AsyncSession


from fastapi import (
    Depends,
    Form,
)


def verify_password(
    password: str,
    hashed_password: bytes
):
    if not check_password(
        password=password,
        hashed_password=hashed_password
    ):
        raise AuthError("Неправильный логин или пароль")
    

def verify_is_active(user: User):
    if not user.is_active:
        raise AuthError(
        status_code=403,
        detail='Пользователь не активен'
    )


async def verify_user(
    session: AsyncSession = Depends(get_db_session), 
    username: str = Form(),
    password: str = Form(),
):
    if not (user:= await UserOperations.get_user(
        session=session,
        searching_parameter='username',
        value=username
    )):
        raise AuthError(detail="Неправильный логин или пароль")

    verify_password(password, user.hashed_password)
    verify_is_active(user)
    return user




    