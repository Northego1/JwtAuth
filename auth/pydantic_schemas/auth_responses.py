from typing import Union
from pydantic import BaseModel, Field


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
    

class AuthResponse200(BaseModel):
    response_status: int
    detail: str | None = None
    token: TokenInfo | None = None
    

class AuthResponse40x(BaseModel):
    response_status: int
    detail: str | None = None
    token: None = None


class ValidationResponseDetails(BaseModel):
    loc: list[Union[str, int]]
    msg: str
    type: str


class ValidationResponse422(BaseModel):
    response_status: int
    detail: list[ValidationResponseDetails]














