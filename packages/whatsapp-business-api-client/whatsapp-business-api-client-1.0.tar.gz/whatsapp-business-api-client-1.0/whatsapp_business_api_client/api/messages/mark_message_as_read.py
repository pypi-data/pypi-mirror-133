from typing import Any, Dict

import httpx

from ...client import Client
from ...models.mark_message_as_read_request import MarkMessageAsReadRequest
from ...types import Response


def _get_kwargs(
    message_id: str,
    *,
    client: Client,
    json_body: MarkMessageAsReadRequest,
) -> Dict[str, Any]:
    url = "{}/messages/{MessageID}".format(client.base_url, MessageID=message_id)

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
    message_id: str,
    *,
    client: Client,
    json_body: MarkMessageAsReadRequest,
) -> Response[Any]:
    """Mark-Message-As-Read

    Args:
        message_id (str):
        json_body (MarkMessageAsReadRequest):  Example: {'status': 'read'}.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        message_id=message_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.put(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    message_id: str,
    *,
    client: Client,
    json_body: MarkMessageAsReadRequest,
) -> Response[Any]:
    """Mark-Message-As-Read

    Args:
        message_id (str):
        json_body (MarkMessageAsReadRequest):  Example: {'status': 'read'}.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        message_id=message_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)
