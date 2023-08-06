from typing import Any, Dict

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    provider_name: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/settings/application/media/providers/{ProviderName}".format(client.base_url, ProviderName=provider_name)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    provider_name: str,
    *,
    client: Client,
) -> Response[Any]:
    """Delete-Media-Providers

    Args:
        provider_name (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        provider_name=provider_name,
        client=client,
    )

    response = httpx.delete(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    provider_name: str,
    *,
    client: Client,
) -> Response[Any]:
    """Delete-Media-Providers

    Args:
        provider_name (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        provider_name=provider_name,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)
