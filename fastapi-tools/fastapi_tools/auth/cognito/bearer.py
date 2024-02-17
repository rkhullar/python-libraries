from .._core import AbstractAuthCodeBearer


class CognitoAuthCodeBearer(AbstractAuthCodeBearer):

    def __init__(self, user_pool_id: str, region: str, scopes: list[str] = None, auto_error: bool = True):
        self.user_pool_id = user_pool_id
        self.region = region
        self.scopes = scopes or ['openid', 'email', 'profile']
        super().__init__(
            authorizationUrl=self.metadata['authorization_endpoint'],
            tokenUrl=self.metadata['token_endpoint'],
            scopes={scope: scope for scope in self.scopes},
            auto_error=auto_error
        )

    @property
    def metadata_url(self) -> str:
        return f'https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/openid-configuration'
