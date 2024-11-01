from fastapi import HTTPException


class AuthError(HTTPException):
    def __init__(
            self,
            status_code: int = 401,
            detail = 'Некорректное имя или пароль',
            headers = None
    ):
        super().__init__(status_code, detail, headers)