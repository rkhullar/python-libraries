from .._core import AbstractAuthCodeBearer


class OktaAuthCodeBearer(AbstractAuthCodeBearer):

    def __init__(self, domain: str, issuer: str = 'default', scopes: list[str] = None, auto_error: bool = True):
        self.domain = domain
        self.issuer = issuer
        self.scopes = scopes or ['openid', 'email', 'profile', 'groups']
        super().__init__(
            authorizationUrl=self.metadata['authorization_endpoint'],
            tokenUrl=self.metadata['token_endpoint'],
            scopes={scope: scope for scope in self.scopes},
            auto_error=auto_error
        )

    @property
    def metadata_url(self) -> str:
        return f'https://{self.domain}/oauth2/{self.issuer}/.well-known/openid-configuration'
