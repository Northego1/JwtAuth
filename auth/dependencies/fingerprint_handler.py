
from fastapi import (
    Depends,
)


from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies.get_current_user import get_user_by_refresh_jwt
from auth.dependencies.db import get_db_session
from auth.dependencies.jwt_getters import get_refresh_jwt_from_cookie
from auth.model import User
from auth.db_repository.users_sessions_CRUD import UserSessionOperations
from auth.utils.finger_print_utils import get_finger_print_hash




async def check_finger_print_jwt(
        refresh_token: str = Depends(get_refresh_jwt_from_cookie),
        user: User = Depends(get_user_by_refresh_jwt),
        finger_print_hash_from_request: str = Depends(get_finger_print_hash),
        session: AsyncSession = Depends(get_db_session)
) -> bool:
    user_session = UserSessionOperations(
        refresh_token=refresh_token,
        user_id=user.id,
        finger_print_hash=finger_print_hash_from_request,
        session=session
    )

    finger_print_hash_from_db = await user_session.get_hash_by_refresh_token()
    if finger_print_hash_from_db != finger_print_hash_from_request:
        await user_session.delete_user_session(fingerprint_hash=finger_print_hash_from_db)
        await user_session.commit_session()
        return False
    return True
    
