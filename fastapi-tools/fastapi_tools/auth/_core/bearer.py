from abc import abstractmethod
from functools import cached_property

import httpx
from fastapi.security import OAuth2AuthorizationCodeBearer

from ...util import BearerAuth, async_httpx


class AbstractAuthCodeBearer(OAuth2AuthorizationCodeBearer):

    @property
    @abstractmethod
    def metadata_url(self) -> str:
        pass

    @cached_property
    def metadata(self) -> dict:
        response = httpx.get(self.metadata_url)
        response.raise_for_status()
        return response.json()

    async def read_user_info(self, access_token: str) -> dict:
        response = await async_httpx(method='get', url=self.metadata['userinfo_endpoint'], auth=BearerAuth(access_token))
        response.raise_for_status()
        return response.json()
