from fastapi import Request



async def get_refresh_jwt_from_cookie(
        request: Request
) -> str | None:
    return request.cookies.get("refresh_jwt")


async def get_access_jwt_from_headers(
        request: Request
) -> str | None:
    return request.headers.get("Authorization")
