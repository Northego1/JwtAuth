from fastapi import (
    Depends,
    Form
)
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies.db import get_db_session
from auth.model import User
from auth.utils.password_utils import hash_password
from auth.db_repository.users import UserOperations


async def user_registration(
        username: str = Form(),
        email: str = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(get_db_session)    
):
    hashed_password = hash_password(password)
    user: User = await UserOperations.create_user(
        session=session,
        username=username,
        hashed_password=hashed_password,
        email=email,
    )
    return user
