from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.message_response import MessageResponse
from ...models.send_text_message_request import SendTextMessageRequest
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: SendTextMessageRequest,
) -> Dict[str, Any]:
    url = "{}/messages".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[MessageResponse]:
    if response.status_code == 200:
        response_200 = MessageResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[MessageResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: SendTextMessageRequest,
) -> Response[MessageResponse]:
    """Send-Message

    Args:
        json_body (SendTextMessageRequest):  Example: {'preview_url': True, 'recipient_type':
            'individual', 'text': {'body': 'your-text-message-content'}, 'to': '{whatsapp-id}',
            'type': 'text'}.

    Returns:
        Response[MessageResponse]
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
    json_body: SendTextMessageRequest,
) -> Optional[MessageResponse]:
    """Send-Message

    Args:
        json_body (SendTextMessageRequest):  Example: {'preview_url': True, 'recipient_type':
            'individual', 'text': {'body': 'your-text-message-content'}, 'to': '{whatsapp-id}',
            'type': 'text'}.

    Returns:
        Response[MessageResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: SendTextMessageRequest,
) -> Response[MessageResponse]:
    """Send-Message

    Args:
        json_body (SendTextMessageRequest):  Example: {'preview_url': True, 'recipient_type':
            'individual', 'text': {'body': 'your-text-message-content'}, 'to': '{whatsapp-id}',
            'type': 'text'}.

    Returns:
        Response[MessageResponse]
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
    json_body: SendTextMessageRequest,
) -> Optional[MessageResponse]:
    """Send-Message

    Args:
        json_body (SendTextMessageRequest):  Example: {'preview_url': True, 'recipient_type':
            'individual', 'text': {'body': 'your-text-message-content'}, 'to': '{whatsapp-id}',
            'type': 'text'}.

    Returns:
        Response[MessageResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
