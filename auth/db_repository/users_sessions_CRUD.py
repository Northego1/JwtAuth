
from datetime import datetime
import email
from typing import Any
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import delete, insert, or_, select, update, func
from auth.exceptions import AuthError
from auth.models import User, UserSession



class UserSessionCrud:
    def __init__(
        self,
        fingerprint_hash: str,
        user_id: int,
        session: AsyncSession,
        refresh_token: str = None,
        expire_at: datetime = None,
    ):
        self.refresh_token: str = refresh_token
        self.finger_print_hash: str = fingerprint_hash
        self.expire_at: datetime = expire_at
        self.user_id: int = user_id
        self.session: AsyncSession = session


    async def create_user_session(self):
        new_record = UserSession(
            refresh_token=self.refresh_token,
            fingerprint_hash=self.finger_print_hash,
            expire_at=self.expire_at,
            user_id=self.user_id
        )
        self.session.add(new_record)


    async def update_user_session(self):
        stmt = (
            update(UserSession)
            .where(
                UserSession.fingerprint_hash == self.finger_print_hash,
                UserSession.user_id == self.user_id
            )
            .values(
                refresh_token=self.refresh_token,
                expire_at=self.expire_at
            )
        )
        await self.session.execute(stmt)


    async def is_session_exist(self) -> bool:
        query = (
            select(UserSession)
            .where(UserSession.fingerprint_hash == self.finger_print_hash)
            .where(UserSession.user_id == self.user_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    

    async def count_user_sessions(self) -> int | None:
        count_query = (
            select(func.count(UserSession.id))
            .where(UserSession.user_id == self.user_id)
            )
        count_result = await self.session.execute(count_query)
        return count_result.scalar()


    async def delete_user_session(self, delete_by: str, value: Any = None):
        if value:
            delete_subquery = (
                select(UserSession.id)
                .where(UserSession.user_id == self.user_id)
                .where(getattr(UserSession, delete_by) == value)
            )
        else:
            delete_subquery = (
                select(UserSession.id)
                .where(UserSession.user_id == self.user_id)
                .order_by(UserSession.expire_at)
                .limit(1)
            )
        delete_stmt = (
            delete(UserSession)
            .where(UserSession.id.in_(delete_subquery)))
        await self.session.execute(delete_stmt)


    async def get_hash_by_refresh_token(self) -> str:
        query = (
            select(UserSession.fingerprint_hash)
            .where(UserSession.user_id == self.user_id) 
            .where(UserSession.refresh_token == self.refresh_token)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def commit_session(self):
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise AuthError(detail=f'Database error {e!r}')
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise AuthError(detail=f'Database error {e!r}')





