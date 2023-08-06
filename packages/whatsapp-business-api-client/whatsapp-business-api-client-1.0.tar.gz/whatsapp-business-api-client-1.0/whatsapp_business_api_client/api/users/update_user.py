from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.root_type_for_user_create_response import RootTypeForUserCreateResponse
from ...models.update_user_request import UpdateUserRequest
from ...types import Response


def _get_kwargs(
    user_username: str,
    *,
    client: Client,
    json_body: UpdateUserRequest,
) -> Dict[str, Any]:
    url = "{}/users/{UserUsername}".format(client.base_url, UserUsername=user_username)

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


def _parse_response(*, response: httpx.Response) -> Optional[RootTypeForUserCreateResponse]:
    if response.status_code == 200:
        response_200 = RootTypeForUserCreateResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[RootTypeForUserCreateResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    user_username: str,
    *,
    client: Client,
    json_body: UpdateUserRequest,
) -> Response[RootTypeForUserCreateResponse]:
    """Update-User

    Args:
        user_username (str):
        json_body (UpdateUserRequest):  Example: {'password': 'New Password'}.

    Returns:
        Response[RootTypeForUserCreateResponse]
    """

    kwargs = _get_kwargs(
        user_username=user_username,
        client=client,
        json_body=json_body,
    )

    response = httpx.put(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    user_username: str,
    *,
    client: Client,
    json_body: UpdateUserRequest,
) -> Optional[RootTypeForUserCreateResponse]:
    """Update-User

    Args:
        user_username (str):
        json_body (UpdateUserRequest):  Example: {'password': 'New Password'}.

    Returns:
        Response[RootTypeForUserCreateResponse]
    """

    return sync_detailed(
        user_username=user_username,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    user_username: str,
    *,
    client: Client,
    json_body: UpdateUserRequest,
) -> Response[RootTypeForUserCreateResponse]:
    """Update-User

    Args:
        user_username (str):
        json_body (UpdateUserRequest):  Example: {'password': 'New Password'}.

    Returns:
        Response[RootTypeForUserCreateResponse]
    """

    kwargs = _get_kwargs(
        user_username=user_username,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    user_username: str,
    *,
    client: Client,
    json_body: UpdateUserRequest,
) -> Optional[RootTypeForUserCreateResponse]:
    """Update-User

    Args:
        user_username (str):
        json_body (UpdateUserRequest):  Example: {'password': 'New Password'}.

    Returns:
        Response[RootTypeForUserCreateResponse]
    """

    return (
        await asyncio_detailed(
            user_username=user_username,
            client=client,
            json_body=json_body,
        )
    ).parsed
