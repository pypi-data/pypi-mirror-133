from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.backup_settings_request import BackupSettingsRequest
from ...models.root_type_for_backup_settings_response import RootTypeForBackupSettingsResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: BackupSettingsRequest,
) -> Dict[str, Any]:
    url = "{}/settings/backup".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[RootTypeForBackupSettingsResponse]:
    if response.status_code == 200:
        response_200 = RootTypeForBackupSettingsResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[RootTypeForBackupSettingsResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: BackupSettingsRequest,
) -> Response[RootTypeForBackupSettingsResponse]:
    """Backup-Settings

    Args:
        json_body (BackupSettingsRequest):  Example: {'password': '<Password for Backup>'}.

    Returns:
        Response[RootTypeForBackupSettingsResponse]
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
    json_body: BackupSettingsRequest,
) -> Optional[RootTypeForBackupSettingsResponse]:
    """Backup-Settings

    Args:
        json_body (BackupSettingsRequest):  Example: {'password': '<Password for Backup>'}.

    Returns:
        Response[RootTypeForBackupSettingsResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: BackupSettingsRequest,
) -> Response[RootTypeForBackupSettingsResponse]:
    """Backup-Settings

    Args:
        json_body (BackupSettingsRequest):  Example: {'password': '<Password for Backup>'}.

    Returns:
        Response[RootTypeForBackupSettingsResponse]
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
    json_body: BackupSettingsRequest,
) -> Optional[RootTypeForBackupSettingsResponse]:
    """Backup-Settings

    Args:
        json_body (BackupSettingsRequest):  Example: {'password': '<Password for Backup>'}.

    Returns:
        Response[RootTypeForBackupSettingsResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
