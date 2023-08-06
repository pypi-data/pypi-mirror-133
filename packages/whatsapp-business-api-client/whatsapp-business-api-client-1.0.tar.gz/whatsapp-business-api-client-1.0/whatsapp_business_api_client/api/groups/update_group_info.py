from typing import Any, Dict

import httpx

from ...client import Client
from ...models.update_group_info_request import UpdateGroupInfoRequest
from ...types import Response


def _get_kwargs(
    group_id: str,
    *,
    client: Client,
    json_body: UpdateGroupInfoRequest,
) -> Dict[str, Any]:
    url = "{}/groups/{GroupId}".format(client.base_url, GroupId=group_id)

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


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    group_id: str,
    *,
    client: Client,
    json_body: UpdateGroupInfoRequest,
) -> Response[Any]:
    """Update-Group-Info

    Args:
        group_id (str):
        json_body (UpdateGroupInfoRequest):  Example: {'subject': '<New Group Subject>'}.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.put(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    group_id: str,
    *,
    client: Client,
    json_body: UpdateGroupInfoRequest,
) -> Response[Any]:
    """Update-Group-Info

    Args:
        group_id (str):
        json_body (UpdateGroupInfoRequest):  Example: {'subject': '<New Group Subject>'}.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)
