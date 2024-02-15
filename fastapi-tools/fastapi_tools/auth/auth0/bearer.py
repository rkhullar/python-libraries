from functools import cached_property

import httpx
from fastapi.security import OAuth2AuthorizationCodeBearer

from ...util import BearerAuth, async_httpx


class Auth0CodeBearer(OAuth2AuthorizationCodeBearer):

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

    @cached_property
    def metadata(self) -> dict:
        response = httpx.get(self.metadata_url)
        response.raise_for_status()
        return response.json()

    async def read_user_info(self, access_token: str) -> dict:
        response = await async_httpx(method='get', url=self.metadata['userinfo_endpoint'], auth=BearerAuth(access_token))
        response.raise_for_status()
        return response.json()
