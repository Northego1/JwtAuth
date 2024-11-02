from fastapi import (
    Depends,
)

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from auth.config import settings
from auth.model import UserSession
from auth.db_repository.users_sessions_CRUD import UserSessionOperations






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




