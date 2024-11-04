from datetime import datetime
from typing import Any
import uuid
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
        jti: uuid.UUID,
        expire_at: datetime,
        session: AsyncSession
    ):
        new_record = BlackListAccessJwt(
            id=jti,
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
    async def read_access_token(
        session: AsyncSession,
        jti: uuid.UUID
    ):
        query = (
            select(BlackListAccessJwt)
            .where(BlackListAccessJwt.id == jti)
        )
        try:
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise AuthError(detail=f'Database error {e!r}')

