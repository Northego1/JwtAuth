from datetime import datetime
import uuid
from pydantic import EmailStr
from sqlalchemy import (
    UUID,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    LargeBinary
)
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True,  nullable=True)
    is_active: Mapped[bool]  = mapped_column(Boolean, nullable=False)

    sessions = relationship( #o2m
        "UserSession",
        back_populates='user'
    )


class UserSession(Base):
    __tablename__ = 'user_session'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    fingerprint_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    refresh_token: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )
    expire_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user = relationship( #m2o
        "User",
        back_populates='sessions'
    )


class BlackListAccessJwt(Base):
    __tablename__ = 'black_list_access_jwt'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4()
        )
    access_token: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )
    expire_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )