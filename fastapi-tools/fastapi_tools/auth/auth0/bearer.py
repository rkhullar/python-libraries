from .._core import AbstractAuthCodeBearer


class Auth0CodeBearer(AbstractAuthCodeBearer):

    def __init__(self, domain: str):
        self.domain = domain
        # TODO: revisit if scopes should be defined
        super().__init__(
            authorizationUrl=self.metadata['authorization_endpoint'],
            tokenUrl=self.metadata['token_endpoint'],
            # scopes={scope: scope for scope in self.scopes}
        )

    @property
    def metadata_url(self) -> str:
        return f'https://{self.domain}/.well-known/openid-configuration'
