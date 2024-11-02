from datetime import datetime
from fastapi import Depends, Form
from auth.config import settings
from sqlalchemy.orm import Session
from auth.dependencies.db import get_db_session
from auth.model import User, UserSession
from auth.db_repository.users_sessions import UserSessionOperations
from auth.utils.password_utils import hash_password
from auth.db_repository.users import UserOperations
from sqlalchemy.ext.asyncio import AsyncSession




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
