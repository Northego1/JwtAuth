import uuid
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import  datetime, timedelta

from auth.config import settings
from auth.dependencies.db import get_db_session
from auth.models import User
from auth.services.user_session_control import control_user_sessions
from auth.utils.jwt_utils import encode_jwt


async def create_refresh_token(
        user: User,
        finger_print_hash: str,
        session: AsyncSession = Depends(get_db_session)
) -> str:
    jwt_payload = {
        "type": "refresh",
        "sub": user.username,
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(
            minutes=settings.jwt.refresh_expire)
    }
    refresh_token = encode_jwt(
        jwt_payload
    )
    await control_user_sessions(
        refresh_token=refresh_token,
        finger_print_hash=finger_print_hash, 
        user_id=user.id,
        expire_at=datetime.utcnow() + timedelta(
            minutes=settings.jwt.refresh_expire),
        session=session
    )
    return refresh_token


def create_access_token(user: User) -> str:
    jwt_payload = {
        "type": "access",
        "sub": user.username,
        "user_id": user.id,
        "email": user.email,
        "jti": str(uuid.uuid4()),
        "exp": datetime.utcnow() + timedelta(
            minutes=settings.jwt.refresh_expire),
    }
    return encode_jwt(
        jwt_payload,
    )