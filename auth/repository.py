
from datetime import datetime
import email
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import or_, select, update, func
from auth.exceptions import AuthError
from auth.model import User, UserSession



class DbUserOperations:
    @staticmethod
    async def get_user(
        session: AsyncSession,
        search_attr: str | int,
    ) -> User | None:
        quary = (
            select(User)
            .where(
                or_(
                    User.username == str(search_attr) if search_attr.isalpha() else None,
                    User.id == int(search_attr) if search_attr.isdigit() else None
                )
            )
        )
        try:
            user = await session.execute(quary)
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
    async def write_user_session(
        refresh_token: str,
        finger_print_hash: str,
        expire_at: datetime,
        user_id: int,
        session: AsyncSession
    ):
        # Проверка на наличие записи с указанным хэшем и user_id
        query = (
            select(UserSession)
            .where(
                UserSession.fingerprint_hash == finger_print_hash,
                UserSession.user_id == user_id
            )
        )
        result = await session.execute(query)
        existing_record = result.scalar_one_or_none()
        
        if existing_record:
            stmt = (
                update(UserSession)
                .where(
                    UserSession.fingerprint_hash == finger_print_hash,
                    UserSession.user_id == user_id
                )
                .values(refresh_token=refresh_token, expire_at=expire_at)
            )
            await session.execute(stmt)
        else:
            new_record = UserSession(
                refresh_token=refresh_token,
                fingerprint_hash=finger_print_hash,
                expire_at=expire_at,
                user_id=user_id
            )
            session.add(new_record)
        try:
            await session.commit()
            if not existing_record:
                await session.refresh(new_record)
            return existing_record if existing_record else new_record
        except IntegrityError as e:
            await session.rollback()
            raise AuthError(detail=f'Database error {e!r}')
        except SQLAlchemyError as e:
            await session.rollback()
            raise AuthError(detail=f'Database error {e!r}')


    @staticmethod
    async def read_user_session():
        pass