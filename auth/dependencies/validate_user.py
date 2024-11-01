from auth.utils.password_utils import check_password
from auth.exceptions import AuthError
from auth.model import User
from auth.repository import db

from fastapi.security import (
    HTTPBearer,
)
from fastapi import (
    Form,
)



def validate_user_auth(
        username: str = Form(),
        password: str = Form(),
) -> User:
    user: User = db.get_user(username=username)
    if not user:
        raise AuthError()
    
    if not check_password(
        password=password,
        hashed_password=user.hashed_password
    ):
        raise AuthError()
    
    if not user.is_active:
        raise AuthError(
            status_code=403,
            detail='Пользователь не активен'
        )
    
    return user






    