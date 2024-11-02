from datetime import datetime
from fastapi import Depends, Form
from auth.config import settings
from sqlalchemy.orm import Session
from auth.db_repository import users_sessions
from auth.dependencies.db import get_db_session
from auth.exceptions import AuthError
from auth.model import User, UserSession
from auth.db_repository.users_sessions import UserSessionOperations
from auth.utils.password_utils import hash_password

from sqlalchemy.ext.asyncio import AsyncSession


async def control_user_sessions(
        refresh_token: str,
        finger_print_hash: str,
        user_id: int,
        expire_at: datetime,
        session: AsyncSession
) -> UserSession:
    
    user_session = UserSessionOperations(
        refresh_token=refresh_token,
        finger_print_hash=finger_print_hash,
        user_id=user_id,
        expire_at=expire_at,
        session=session
    )

    if await user_session.is_session_exist():
        await user_session.update_user_session()
    else:
        if await user_session.count_user_sessions() < settings.jwt.max_user_sessions:
            await user_session.create_user_session()
        else:
            await user_session.delete_user_session()
            await user_session.create_user_session()


    await user_session.commit_session()



async def check_fingeprint_jwt(
        refresh_token: str,
        finger_print_hash_from_request: str,
        user_id: int,
        session: AsyncSession 
) -> bool:
    user_session = UserSessionOperations(
        refresh_token=refresh_token,
        user_id=user_id,
        session=session
    )

    finger_print_hash_from_db = await user_session.get_hash_by_refresh_token()
    if finger_print_hash_from_db != finger_print_hash_from_request:
        user_session.delete_user_session(fingerprint_hash=finger_print_hash_from_db)
        raise AuthError()
    

