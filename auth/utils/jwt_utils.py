import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import  datetime, timedelta
from typing import Optional

from auth.config import settings
from auth.exceptions import AuthError



def encode_jwt(
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