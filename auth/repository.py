from abc import ABC, abstractmethod
import email
from pydantic import EmailStr

from auth.model import User


class db:
    @staticmethod
    def get_user(
            username: str,
    ) -> User | None:
        
        if username == 'John':
            return User(
                id=1,
                username='John',
                hashed_password=b'$2b$12$eIG7rlZpTrV36cla8sBqLuoGHIDXnDT.4XzF0lXYNV4229eGTKOpG',
                email='John@gmail.com',
                is_active=True
            )

    @staticmethod
    def create_user(
            username: str,
            password: bytes,
            email: EmailStr,
            is_active: bool
    ) -> User | None:
        pass


    def update_user(
            self,
            user_id: int,
    ):
        pass