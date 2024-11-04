from datetime import datetime
from typing import Any
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select
from auth.exceptions import AuthError
from auth.models import BlackListAccessJwt


class BlackListCrud:
    @staticmethod
    async def add_access_token(
        access_token: str,
        expire_at: datetime,
        session: AsyncSession
    ):
        new_record = BlackListAccessJwt(
            access_token=access_token,
            expire_at=datetime.utcfromtimestamp(expire_at)
        )
        session.add(new_record)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise AuthError(
                status_code=400,
                detail=f'Something went wrong'
            )
        except SQLAlchemyError as e:
            raise AuthError(detail=f'{e}')


    @staticmethod
    async def read_access_jwt_from_black_list():
        pass


