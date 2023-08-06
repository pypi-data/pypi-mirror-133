from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.group_response import GroupResponse
from ...types import Response


def _get_kwargs(
    group_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/groups/{GroupId}".format(client.base_url, GroupId=group_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[GroupResponse]:
    if response.status_code == 200:
        response_200 = GroupResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[GroupResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    group_id: str,
    *,
    client: Client,
) -> Response[GroupResponse]:
    """Get-Group-Info

    Args:
        group_id (str):

    Returns:
        Response[GroupResponse]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    group_id: str,
    *,
    client: Client,
) -> Optional[GroupResponse]:
    """Get-Group-Info

    Args:
        group_id (str):

    Returns:
        Response[GroupResponse]
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    group_id: str,
    *,
    client: Client,
) -> Response[GroupResponse]:
    """Get-Group-Info

    Args:
        group_id (str):

    Returns:
        Response[GroupResponse]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    group_id: str,
    *,
    client: Client,
) -> Optional[GroupResponse]:
    """Get-Group-Info

    Args:
        group_id (str):

    Returns:
        Response[GroupResponse]
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
        )
    ).parsed
