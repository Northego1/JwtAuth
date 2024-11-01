from auth.config import settings
from sqlalchemy.orm import Session
from auth.repository import DbUserOperations


def get_user(user_id: int):
    pass




def write_fingeprint_jwt_to_db(
        refresh_token: str,
        finger_print_hash: str,
        user_id: int,
        db_session: Session
) -> bool:
    DbUserOperations.write_user_session(
        refresh_token,
        finger_print_hash,
        user_id,
        db_session
    )
    return


def check_fingeprint_jwt(
        refresh_token: str,
        finger_print_hash: str,
        user_id: int,
        db_session: Session 
) -> bool:
    pass