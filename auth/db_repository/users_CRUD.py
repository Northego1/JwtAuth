
from datetime import datetime
from typing import Any
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select
from auth.exceptions import AuthError
from auth.models import User


class UserCrud:
    @staticmethod
    async def get_user(
        session: AsyncSession,
        searching_parameter: Any,
        value: Any
    ) -> User | None:
        query = (
            select(User)
            .where(getattr(User, searching_parameter) == value)
        )
        try:
            user = await session.execute(query)
            user = user.scalar_one_or_none()
            return user
        except SQLAlchemyError as e:
            raise AuthError(detail=f'Database error {e!r}')
        

    @staticmethod
    async def create_user(
        session: AsyncSession,
        username: str,
        hashed_password: bytes,
        email: EmailStr
    ) -> User:
        new_user = User(
            username=username,
            hashed_password=hashed_password,
            email=email,
            is_active=True
        )
        session.add(new_user)
        try:
            await session.commit()
            await session.refresh(new_user)
            return new_user
        except IntegrityError:
            await session.rollback()
            raise AuthError(
                status_code=400,
                detail=f'Имя пользователя {username} занято'
            )
        except SQLAlchemyError as e:
            raise AuthError('Database error {e!r}')


    @staticmethod
    def update_user(
            user_id: int,
    ):
        pass


    @staticmethod
    def delete_user():
        pass
