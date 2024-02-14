from dataclasses import dataclass

import httpx


async def async_httpx(method: str, *args, verify: bool = True, **kwargs):
    async with httpx.AsyncClient(verify=verify) as client:
        fn = getattr(client, method)
        return await fn(*args, **kwargs)


@dataclass
class BearerAuth(httpx.Auth):
    token: str

    def auth_flow(self, request):
        request.headers['Authorization'] = f'Bearer {self.token}'
        yield request
