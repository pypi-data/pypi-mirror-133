from typing import Any, Dict

import httpx

from ...client import Client
from ...models.group_id_icon_body import GroupIdIconBody
from ...types import Response


def _get_kwargs(
    group_id: str,
    *,
    client: Client,
    multipart_data: GroupIdIconBody,
) -> Dict[str, Any]:
    url = "{}/groups/{GroupId}/icon".format(client.base_url, GroupId=group_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
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
    multipart_data: GroupIdIconBody,
) -> Response[Any]:
    """Set-Group-Icon

    Args:
        group_id (str):
        multipart_data (GroupIdIconBody):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
        multipart_data=multipart_data,
    )

    response = httpx.post(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    group_id: str,
    *,
    client: Client,
    multipart_data: GroupIdIconBody,
) -> Response[Any]:
    """Set-Group-Icon

    Args:
        group_id (str):
        multipart_data (GroupIdIconBody):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
        multipart_data=multipart_data,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)
