from typing import Any, Dict

import httpx

from ...client import Client
from ...models.set_shards_request import SetShardsRequest
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: SetShardsRequest,
) -> Dict[str, Any]:
    url = "{}/account/shards".format(client.base_url)

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
    *,
    client: Client,
    json_body: SetShardsRequest,
) -> Response[Any]:
    """Set-Shards

    Args:
        json_body (SetShardsRequest):  Example: {'cc': '<Country Code>', 'phone_number': '<Phone
            Number>', 'pin': '<Two-Step PIN>', 'shards': 32}.

    Returns:
        Response[Any]
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


async def asyncio_detailed(
    *,
    client: Client,
    json_body: SetShardsRequest,
) -> Response[Any]:
    """Set-Shards

    Args:
        json_body (SetShardsRequest):  Example: {'cc': '<Country Code>', 'phone_number': '<Phone
            Number>', 'pin': '<Two-Step PIN>', 'shards': 32}.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)
