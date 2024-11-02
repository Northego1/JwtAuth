from fastapi import Depends
import jwt
from datetime import  datetime, timedelta
from typing import Optional
from auth.config import settings
from auth.dependencies.db import get_db_session
from auth.exceptions import AuthError
from auth.model import User
from auth.services.session_control import control_user_sessions
from sqlalchemy.ext.asyncio import AsyncSession

def create_jwt(
        payload: dict,
        private_key: str = settings.jwt.private_key.read_text()
) -> str:
    payload_copy = payload.copy()
    encoded_jwt = jwt.encode(
        payload_copy,
        private_key,
        algorithm=settings.jwt.alghoritm 
    )
    return encoded_jwt


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.jwt.public_key.read_text()
) -> Optional[dict]:
    try:
        payload: dict = jwt.decode(
            token,
            public_key, 
            algorithms=settings.jwt.alghoritm
        )
        return payload
    except jwt.PyJWTError:
        raise AuthError(detail='Токен некорректен или просрочен')
    

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
    refresh_token = create_jwt(
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
        "exp": datetime.utcnow() + timedelta(
            minutes=settings.jwt.refresh_expire)
    }
    return create_jwt(
        jwt_payload,
    )