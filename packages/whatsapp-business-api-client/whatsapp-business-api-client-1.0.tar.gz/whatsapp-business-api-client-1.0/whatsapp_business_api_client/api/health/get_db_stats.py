from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.get_db_stats_response_200 import GetDbStatsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    format_: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/stats/db".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "format": format_,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[GetDbStatsResponse200]:
    if response.status_code == 200:
        response_200 = GetDbStatsResponse200.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[GetDbStatsResponse200]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    format_: Union[Unset, None, str] = UNSET,
) -> Response[GetDbStatsResponse200]:
    """Get-DB-Stats

    Args:
        format_ (Union[Unset, None, str]):

    Returns:
        Response[GetDbStatsResponse200]
    """

    kwargs = _get_kwargs(
        client=client,
        format_=format_,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    format_: Union[Unset, None, str] = UNSET,
) -> Optional[GetDbStatsResponse200]:
    """Get-DB-Stats

    Args:
        format_ (Union[Unset, None, str]):

    Returns:
        Response[GetDbStatsResponse200]
    """

    return sync_detailed(
        client=client,
        format_=format_,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    format_: Union[Unset, None, str] = UNSET,
) -> Response[GetDbStatsResponse200]:
    """Get-DB-Stats

    Args:
        format_ (Union[Unset, None, str]):

    Returns:
        Response[GetDbStatsResponse200]
    """

    kwargs = _get_kwargs(
        client=client,
        format_=format_,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    format_: Union[Unset, None, str] = UNSET,
) -> Optional[GetDbStatsResponse200]:
    """Get-DB-Stats

    Args:
        format_ (Union[Unset, None, str]):

    Returns:
        Response[GetDbStatsResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            format_=format_,
        )
    ).parsed
