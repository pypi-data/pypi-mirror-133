from typing import Any, Dict

import httpx

from ...client import Client
from ...models.set_business_profile_request import SetBusinessProfileRequest
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: SetBusinessProfileRequest,
) -> Dict[str, Any]:
    url = "{}/settings/business/profile".format(client.base_url)

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
    json_body: SetBusinessProfileRequest,
) -> Response[Any]:
    """Update-Business-Profile

    Args:
        json_body (SetBusinessProfileRequest):  Example: {'address': '<Business Profile Address>',
            'description': '<Business Profile Description>', 'email': '<Business Profile Email>',
            'vertical': '<Business Profile Vertical>', 'websites': ['https://www.whatsapp.com',
            'https://www.facebook.com']}.

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
    json_body: SetBusinessProfileRequest,
) -> Response[Any]:
    """Update-Business-Profile

    Args:
        json_body (SetBusinessProfileRequest):  Example: {'address': '<Business Profile Address>',
            'description': '<Business Profile Description>', 'email': '<Business Profile Email>',
            'vertical': '<Business Profile Vertical>', 'websites': ['https://www.whatsapp.com',
            'https://www.facebook.com']}.

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
