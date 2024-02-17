from pydantic import BaseModel


class CognitoIdentityToken(BaseModel):
    sub: str
    email_verified: bool
    given_name: str
    family_name: str
    email: str
    username: str
