from typing import Optional

from pydantic import BaseModel


class Auth0IdentityToken(BaseModel):
    sub: str
    given_name: str
    family_name: str
    nickname: str
    name: str
    picture: str
    locale: Optional[str] = None
    updated_at: str  # datetime
    email: str
    email_verified: bool
