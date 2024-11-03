from fastapi import FastAPI

from auth.exceptions import AuthError
from auth.pydantic_schemas.auth_responses import AuthResponse40x, ValidationResponse422
from auth.router import router as auth_router
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ValidationException


app = FastAPI()

app.include_router(router=auth_router)



@app.exception_handler(AuthError)
async def auth_exception_handler(
    request: Request,
    exc: AuthError
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=AuthResponse40x(
            response_status=exc.status_code,
            detail=exc.detail
        ).model_dump()
    )



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=ValidationResponse422(
            response_status=422,
            detail=exc.errors(),
        ).model_dump()
    )

