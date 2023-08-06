from typing import Any, Dict

import httpx

from ...client import Client
from ...models.set_profile_about_request import SetProfileAboutRequest
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: SetProfileAboutRequest,
) -> Dict[str, Any]:
    url = "{}/settings/profile/about".format(client.base_url)

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
    json_body: SetProfileAboutRequest,
) -> Response[Any]:
    """Update-Profile-About

    Args:
        json_body (SetProfileAboutRequest):  Example: {'text': '<About Profile>'}.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.patch(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: Client,
    json_body: SetProfileAboutRequest,
) -> Response[Any]:
    """Update-Profile-About

    Args:
        json_body (SetProfileAboutRequest):  Example: {'text': '<About Profile>'}.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)
