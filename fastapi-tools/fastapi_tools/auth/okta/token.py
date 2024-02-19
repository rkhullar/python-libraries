from pydantic import BaseModel


class OktaIdentityToken(BaseModel):
    sub: str
    name: str
    locale: str
    email: str
    preferred_username: str
    given_name: str
    family_name: str
    zoneinfo: str
    email_verified: bool
    groups: list[str]
