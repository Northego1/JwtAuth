from datetime import datetime
from fastapi import Depends, Form
from auth.config import settings
from sqlalchemy.orm import Session
from auth.dependencies.db import get_db_session
from auth.model import User, UserSession
from auth.repository import DbUserOperations
from auth.utils.password_utils import hash_password

from sqlalchemy.ext.asyncio import AsyncSession
from auth.repository import DbUserOperations


def get_user(user_id: int):
    pass


async def write_fingeprint_jwt_to_db(
        refresh_token: str,
        finger_print_hash: str,
        user_id: int,
        expire_at: datetime,
        session: AsyncSession
) -> UserSession:
    return await DbUserOperations.write_user_session(
        refresh_token=refresh_token,
        finger_print_hash=finger_print_hash,
        expire_at=expire_at,
        user_id=user_id,
        session=session
    )



def check_fingeprint_jwt(
        refresh_token: str,
        finger_print_hash: str,
        user_id: int,
        db_session: Session 
) -> bool:
    pass


async def register_user(
        username: str = Form(),
        email: str = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(get_db_session)    
):
    hashed_password = hash_password(password)
    user: User = await DbUserOperations.create_user(
        session=session,
        username=username,
        hashed_password=hashed_password,
        email=email,
    )
    return user


