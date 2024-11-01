from datetime import datetime
from pydantic import EmailStr
from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True,  nullable=True)
    is_active: Mapped[bool]  = mapped_column(Boolean, nullable=False)



class UserSession(Base):
    __tablename__ = 'user_session'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fingerprint_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True  
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    refresh_token: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )
    expire_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


