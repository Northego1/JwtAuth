from abc import ABC, abstractmethod
import email
from pydantic import EmailStr
from sqlalchemy.orm import Session


from auth.model import User, UserSession


class DbUserOperations:
    @staticmethod
    def get_user(
            search_attr,
    ) -> User | None:
        print(f'{search_attr=}')
        if search_attr == 'John' or search_attr == 1:
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


    @staticmethod
    def update_user(
            user_id: int,
    ):
        pass

    
    @staticmethod
    def write_user_session(
        refresh_token: str,
        finger_print_hash: str,
        user_id: int,
        db_session: Session
    ):
        record = UserSession(
            refresh_token=refresh_token,
            fingerprint_hash = finger_print_hash,
            user_id=user_id     
        )
        return record