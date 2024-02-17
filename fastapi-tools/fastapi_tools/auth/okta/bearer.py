from functools import cached_property
import httpx
from fastapi.security import OAuth2AuthorizationCodeBearer
from ...util import BearerAuth, async_httpx


class OktaAuthCodeBearer(OAuth2AuthorizationCodeBearer):

    def __init__(self, domain: str, issuer: str = 'default'):
        self.domain = domain
        self.issuer = issuer
        scopes = ['openid', 'email', 'profile']
        super().__init__(
            authorizationUrl=self.metadata['authorization_endpoint'],
            tokenUrl=self.metadata['token_endpoint'],
            scopes={scope: scope for scope in scopes}
        )

    @property
    def metadata_url(self) -> str:
        return f'https://{self.domain}/oauth2/{self.issuer}/.well-known/openid-configuration'

    @cached_property
    def metadata(self) -> dict:
        response = httpx.get(self.metadata_url)
        response.raise_for_status()
        return response.json()

    async def read_user_info(self, access_token: str) -> dict:
        response = await async_httpx(method='get', url=self.metadata['userinfo_endpoint'], auth=BearerAuth(access_token))
        response.raise_for_status()
        return response.json()
