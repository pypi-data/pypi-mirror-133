from typing import Any, Dict, Optional

import httpx

from ...client import AuthenticatedClient
from ...models.login_admin_request import LoginAdminRequest
from ...models.user_login_response import UserLoginResponse
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: LoginAdminRequest,
) -> Dict[str, Any]:
    url = "{}/users/login".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[UserLoginResponse]:
    if response.status_code == 200:
        response_200 = UserLoginResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[UserLoginResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: LoginAdminRequest,
) -> Response[UserLoginResponse]:
    """Login-User

    Args:
        json_body (LoginAdminRequest):  Example: {'new_password': '<New Admin Password>'}.

    Returns:
        Response[UserLoginResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: LoginAdminRequest,
) -> Optional[UserLoginResponse]:
    """Login-User

    Args:
        json_body (LoginAdminRequest):  Example: {'new_password': '<New Admin Password>'}.

    Returns:
        Response[UserLoginResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: LoginAdminRequest,
) -> Response[UserLoginResponse]:
    """Login-User

    Args:
        json_body (LoginAdminRequest):  Example: {'new_password': '<New Admin Password>'}.

    Returns:
        Response[UserLoginResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: LoginAdminRequest,
) -> Optional[UserLoginResponse]:
    """Login-User

    Args:
        json_body (LoginAdminRequest):  Example: {'new_password': '<New Admin Password>'}.

    Returns:
        Response[UserLoginResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
