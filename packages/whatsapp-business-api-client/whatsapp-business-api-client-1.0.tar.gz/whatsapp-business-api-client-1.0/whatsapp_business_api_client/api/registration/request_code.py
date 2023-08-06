from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.request_code_request import RequestCodeRequest
from ...models.root_type_for_request_code_response import RootTypeForRequestCodeResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: RequestCodeRequest,
) -> Dict[str, Any]:
    url = "{}/account".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, RootTypeForRequestCodeResponse]]:
    if response.status_code == 201:
        response_201 = None

        return response_201
    if response.status_code == 202:
        response_202 = RootTypeForRequestCodeResponse.from_dict(response.json())

        return response_202
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, RootTypeForRequestCodeResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: RequestCodeRequest,
) -> Response[Union[Any, RootTypeForRequestCodeResponse]]:
    """Request-Code

    Args:
        json_body (RequestCodeRequest):  Example: {'cc': '<Country Code>', 'cert': '<Valid Cert
            from Business Manager>', 'method': '< sms | voice >', 'phone_number': '<Phone Number>',
            'pin': '<Two-Step Verification PIN'}.

    Returns:
        Response[Union[Any, RootTypeForRequestCodeResponse]]
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


def sync(
    *,
    client: Client,
    json_body: RequestCodeRequest,
) -> Optional[Union[Any, RootTypeForRequestCodeResponse]]:
    """Request-Code

    Args:
        json_body (RequestCodeRequest):  Example: {'cc': '<Country Code>', 'cert': '<Valid Cert
            from Business Manager>', 'method': '< sms | voice >', 'phone_number': '<Phone Number>',
            'pin': '<Two-Step Verification PIN'}.

    Returns:
        Response[Union[Any, RootTypeForRequestCodeResponse]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: RequestCodeRequest,
) -> Response[Union[Any, RootTypeForRequestCodeResponse]]:
    """Request-Code

    Args:
        json_body (RequestCodeRequest):  Example: {'cc': '<Country Code>', 'cert': '<Valid Cert
            from Business Manager>', 'method': '< sms | voice >', 'phone_number': '<Phone Number>',
            'pin': '<Two-Step Verification PIN'}.

    Returns:
        Response[Union[Any, RootTypeForRequestCodeResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: RequestCodeRequest,
) -> Optional[Union[Any, RootTypeForRequestCodeResponse]]:
    """Request-Code

    Args:
        json_body (RequestCodeRequest):  Example: {'cc': '<Country Code>', 'cert': '<Valid Cert
            from Business Manager>', 'method': '< sms | voice >', 'phone_number': '<Phone Number>',
            'pin': '<Two-Step Verification PIN'}.

    Returns:
        Response[Union[Any, RootTypeForRequestCodeResponse]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
