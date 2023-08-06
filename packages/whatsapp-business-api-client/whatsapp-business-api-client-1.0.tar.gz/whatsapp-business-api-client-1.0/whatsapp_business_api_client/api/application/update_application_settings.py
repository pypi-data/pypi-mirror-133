from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.response import Response
from ...models.update_application_settings_request_body import UpdateApplicationSettingsRequestBody
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: UpdateApplicationSettingsRequestBody,
) -> Dict[str, Any]:
    url = "{}/settings/application".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Response]:
    if response.status_code == 200:
        response_200 = Response.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Response]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: UpdateApplicationSettingsRequestBody,
) -> Response[Response]:
    """Update-Application-Settings

     If a field is not present in the request, no change is made to that setting. For example, if
    on_call_pager is not sent with the request, the existing configuration for on_call_pager is
    unchanged.

    Args:
        json_body (UpdateApplicationSettingsRequestBody):  Example: {'callback_backoff_delay_ms':
            3000, 'callback_persist': True, 'max_callback_backoff_delay_ms': 900000, 'media':
            {'auto_download': ['image', 'document', 'audio']}, 'on_call_pager': '<WA_ID of valid
            WhatsApp contact>', 'pass_through': False, 'sent_status': False, 'webhooks':
            {'max_concurrent_requests': 12, 'url': '<Webhook URL, https>'}}.

    Returns:
        Response[Response]
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


def sync(
    *,
    client: Client,
    json_body: UpdateApplicationSettingsRequestBody,
) -> Optional[Response]:
    """Update-Application-Settings

     If a field is not present in the request, no change is made to that setting. For example, if
    on_call_pager is not sent with the request, the existing configuration for on_call_pager is
    unchanged.

    Args:
        json_body (UpdateApplicationSettingsRequestBody):  Example: {'callback_backoff_delay_ms':
            3000, 'callback_persist': True, 'max_callback_backoff_delay_ms': 900000, 'media':
            {'auto_download': ['image', 'document', 'audio']}, 'on_call_pager': '<WA_ID of valid
            WhatsApp contact>', 'pass_through': False, 'sent_status': False, 'webhooks':
            {'max_concurrent_requests': 12, 'url': '<Webhook URL, https>'}}.

    Returns:
        Response[Response]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: UpdateApplicationSettingsRequestBody,
) -> Response[Response]:
    """Update-Application-Settings

     If a field is not present in the request, no change is made to that setting. For example, if
    on_call_pager is not sent with the request, the existing configuration for on_call_pager is
    unchanged.

    Args:
        json_body (UpdateApplicationSettingsRequestBody):  Example: {'callback_backoff_delay_ms':
            3000, 'callback_persist': True, 'max_callback_backoff_delay_ms': 900000, 'media':
            {'auto_download': ['image', 'document', 'audio']}, 'on_call_pager': '<WA_ID of valid
            WhatsApp contact>', 'pass_through': False, 'sent_status': False, 'webhooks':
            {'max_concurrent_requests': 12, 'url': '<Webhook URL, https>'}}.

    Returns:
        Response[Response]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: UpdateApplicationSettingsRequestBody,
) -> Optional[Response]:
    """Update-Application-Settings

     If a field is not present in the request, no change is made to that setting. For example, if
    on_call_pager is not sent with the request, the existing configuration for on_call_pager is
    unchanged.

    Args:
        json_body (UpdateApplicationSettingsRequestBody):  Example: {'callback_backoff_delay_ms':
            3000, 'callback_persist': True, 'max_callback_backoff_delay_ms': 900000, 'media':
            {'auto_download': ['image', 'document', 'audio']}, 'on_call_pager': '<WA_ID of valid
            WhatsApp contact>', 'pass_through': False, 'sent_status': False, 'webhooks':
            {'max_concurrent_requests': 12, 'url': '<Webhook URL, https>'}}.

    Returns:
        Response[Response]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
