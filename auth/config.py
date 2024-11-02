from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
BASE_DIR = Path(__file__).resolve().parents[1]


class AuthJwt(BaseModel):
    private_key: Path = BASE_DIR / "auth" / "jwt_certs" / "jwt-private.pem"
    public_key: Path = BASE_DIR / "auth" / "jwt_certs" / "jwt-public.pem"
    alghoritm: str = "RS256"

    type_field: str = "type"
    access_type: str = "access"
    refresh_type: str = "refresh"

    refresh_expire: int = 43200 # 30 days
    access_expire: int = 10

    max_user_sessions: int = 5

class Settings(BaseSettings):
    jwt: AuthJwt = AuthJwt()


settings = Settings()