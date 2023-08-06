from datetime import datetime
import asyncio, base64
import attr
from httpx import RequestError

from whatsapp_business_api_client import (
    AuthenticatedClient
)

from whatsapp_business_api_client.api.users import (
    login_user,
)

from whatsapp_business_api_client.models import (
    UserLoginResponse,
    LoginAdminRequest
)

@attr.s(auto_attribs=True)
class ClientWrapper(AuthenticatedClient):

    async def renew_token(self, login_client = AuthenticatedClient):
        try:
            response: UserLoginResponse = await login_user.asyncio(client=login_client, json_body=LoginAdminRequest(""))
            token = response.users[0].token
            until = response.users[0].expires_after
            delta = abs(until - datetime.now())
            return {
                "token": token,
                "valid_for": delta.seconds
            }

        except RequestError as e:
            raise e # rethrow, fail fast
        

    async def run_manage_token(self, login_client = AuthenticatedClient, loop = None, delay: int = 10, delay_factor: float = 0.8):
        loop = loop or asyncio.get_event_loop()
        while loop.is_running():
            try:
                response = await self.renew_token(login_client)
                delay = response.valid_for * delay_factor
                self.token = response.token

            except RequestError as e:
                print(e)
                delay = 10

            print(f'Delay set to {delay}')
            await asyncio.sleep(delay)

    async def manage_token(self, username: str, password: str):
        basic_auth = f"{username}:{password}"
        basic_auth_bytes = basic_auth.encode('ascii')
        basic_auth_b64 = base64.b64encode(basic_auth_bytes)
        login_client = self.with_headers({"Authorization": f"Basic {basic_auth_b64}"})
        await self.renew_token(login_client) # throws, fail fast
         
        asyncio.create_task(self.run_manage_token(login_client))

    @classmethod
    async def with_managed_token(cls, base_url: str, username: str, password: str):
        client = cls(base_url, "")
        await client.manage_token(username, password)
        return client
