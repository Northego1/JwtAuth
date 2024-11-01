from auth.utils.password_utils import check_password
from auth.exceptions import AuthError
from auth.model import User
from auth.repository import DbUserOperations


from fastapi import (
    Form,
)

class ValidateUser:
    def __init__(   
        self,     
        username: str = Form(),
        password: str = Form()
    ):
        self.username: str = username
        self.password: str = password
        self.user: User = DbUserOperations.get_user(search_attr=username)

    def __call__(self):
        if not self.user:
            raise AuthError()
        self.verify_password()
        self.verify_is_active()
        return self.user


    def verify_password(self):
        if not check_password(
            password=self.password,
            hashed_password=self.user.hashed_password
        ):
            raise AuthError()
        
    def verify_is_active(self):
        if not self.user.is_active:
            raise AuthError(
            status_code=403,
            detail='Пользователь не активен'
        )







    