from datetime import datetime
import uuid
from auth.db_repository import black_list_access_CRUD
from auth.db_repository.black_list_access_CRUD import BlackListCrud
from sqlalchemy.ext.asyncio import AsyncSession

from auth.db_repository.users_sessions_CRUD import UserSessionCrud


class LogoutControl:
    def __init__(
            self,
            access_jwt_payload: dict,
            session: AsyncSession
        ):
        self.access_jwt_payload: dict = access_jwt_payload
        self.user_id = access_jwt_payload.get('user_id')
        self.session: AsyncSession = session


    async def add_access_token_to_black_list(
            self,
            access_token: str,
        ):
        expire_at: datetime = self.access_jwt_payload.get('exp')
        jti: uuid.UUID = self.access_jwt_payload.get('jti')
        await BlackListCrud.add_access_token(
            access_token=access_token,
            jti=jti,
            expire_at=expire_at,
            session=self.session
        )
        
        
    async def revoke_refresh_token(
        self,
        fingerprint_hash: str,
    ):
        user_session = UserSessionCrud(
            fingerprint_hash=fingerprint_hash,
            user_id=self.user_id,
            session=self.session
        )
        await user_session.delete_user_session(
            'fingerprint_hash',
            fingerprint_hash
        )
        await user_session.commit_session()