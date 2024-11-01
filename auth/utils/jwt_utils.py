import jwt
from datetime import  datetime, timedelta
from typing import Optional
from auth.config import settings
from auth.exceptions import AuthError
from auth.model import User


def create_jwt(
        payload: dict,
        expires_delta_minutes: int,
        private_key: str = settings.jwt.private_key.read_text()
) -> str:
    
    payload_copy = payload.copy()
    payload_copy.update(
        exp=datetime.utcnow() + timedelta(minutes=expires_delta_minutes)
    )
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
    

def create_refresh_token(user: User):
    jwt_payload = {
        "type": "refresh",
        "sub": user.username,
        "user_id": user.id,
        "email": user.email
    }
    return create_jwt(
        jwt_payload,
        expires_delta_minutes=settings.jwt.refresh_expire
    )


def create_access_token(user: User):
    jwt_payload = {
        "type":  "access",
        "sub": user.username,
        "user_id": user.id
    }
    return create_jwt(
        jwt_payload,
        expires_delta_minutes=settings.jwt.refresh_expire
    )