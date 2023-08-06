from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.media import Media
from ..models.webhooks import Webhooks
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateApplicationSettingsRequestBody")


@attr.s(auto_attribs=True)
class UpdateApplicationSettingsRequestBody:
    """
    Example:
        {'callback_backoff_delay_ms': 3000, 'callback_persist': True, 'max_callback_backoff_delay_ms': 900000, 'media':
            {'auto_download': ['image', 'document', 'audio']}, 'on_call_pager': '<WA_ID of valid WhatsApp contact>',
            'pass_through': False, 'sent_status': False, 'webhooks': {'max_concurrent_requests': 12, 'url': '<Webhook URL,
            https>'}}

    Attributes:
        callback_backoff_delay_ms (Union[Unset, str]): Backoff delay for a failed callback in milliseconds
            This setting is used to configure the amount of time the backoff delays before retrying a failed callback. The
            backoff delay increases linearly by this value each time a callback fails to get a HTTPS 200 OK response. The
            backoff delay is capped by the max_callback_backoff_delay_ms setting. Default: '3000'.
        callback_persist (Union[Unset, bool]): Stores callbacks on disk until they are successfully acknowledged by the
            Webhook or not. Restart required. Default: True.
        heartbeat_interval (Union[Unset, int]): Multiconnect: Interval of the Master node monitoring of Coreapp nodes in
            seconds Default: 5.
        max_callback_backoff_delay_ms (Union[Unset, str]): Maximum delay for a failed callback in milliseconds Default:
            '900000'.
        media (Union[Unset, Media]):  Example: {'auto_download': ['image', 'document', 'audio']}.
        on_call_pager (Union[Unset, str]): Set to valid WhatsApp Group with users who wish to see alerts for critical
            errors and messages.
        pass_through (Union[Unset, bool]): When true, removes messages from the local database after they are delivered
            to or read by the recipient. When false, saves all messages on local storage until they are explicitly deleted.
            When messages are sent, they are stored in a local database. This database is used as the application's history.
            Since the business keeps its own history, you can specify whether you want message pass_through or not. Restart
            required. Default: True.
        sent_status (Union[Unset, bool]): Receive a notification that a message is sent to server. When true, you will
            receive a message indicating that a message has been sent. If false (default), you will not receive
            notification.
        unhealthy_interval (Union[Unset, int]): Multiconnect: Maximum amount of seconds a Master node waits for a
            Coreapp node to respond to a heartbeat before considering it unhealthy and starting the failover process.
            Default: 30.
        webhooks (Union[Unset, Webhooks]):  Example: {'max_concurrent_requests': 12, 'url': '<Webhook URL, https>'}.
    """

    callback_backoff_delay_ms: Union[Unset, str] = "3000"
    callback_persist: Union[Unset, bool] = True
    heartbeat_interval: Union[Unset, int] = 5
    max_callback_backoff_delay_ms: Union[Unset, str] = "900000"
    media: Union[Unset, Media] = UNSET
    on_call_pager: Union[Unset, str] = UNSET
    pass_through: Union[Unset, bool] = True
    sent_status: Union[Unset, bool] = False
    unhealthy_interval: Union[Unset, int] = 30
    webhooks: Union[Unset, Webhooks] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        callback_backoff_delay_ms = self.callback_backoff_delay_ms
        callback_persist = self.callback_persist
        heartbeat_interval = self.heartbeat_interval
        max_callback_backoff_delay_ms = self.max_callback_backoff_delay_ms
        media: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.media, Unset):
            media = self.media.to_dict()

        on_call_pager = self.on_call_pager
        pass_through = self.pass_through
        sent_status = self.sent_status
        unhealthy_interval = self.unhealthy_interval
        webhooks: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.webhooks, Unset):
            webhooks = self.webhooks.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if callback_backoff_delay_ms is not UNSET:
            field_dict["callback_backoff_delay_ms"] = callback_backoff_delay_ms
        if callback_persist is not UNSET:
            field_dict["callback_persist"] = callback_persist
        if heartbeat_interval is not UNSET:
            field_dict["heartbeat_interval"] = heartbeat_interval
        if max_callback_backoff_delay_ms is not UNSET:
            field_dict["max_callback_backoff_delay_ms"] = max_callback_backoff_delay_ms
        if media is not UNSET:
            field_dict["media"] = media
        if on_call_pager is not UNSET:
            field_dict["on_call_pager"] = on_call_pager
        if pass_through is not UNSET:
            field_dict["pass_through"] = pass_through
        if sent_status is not UNSET:
            field_dict["sent_status"] = sent_status
        if unhealthy_interval is not UNSET:
            field_dict["unhealthy_interval"] = unhealthy_interval
        if webhooks is not UNSET:
            field_dict["webhooks"] = webhooks

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        callback_backoff_delay_ms = d.pop("callback_backoff_delay_ms", UNSET)

        callback_persist = d.pop("callback_persist", UNSET)

        heartbeat_interval = d.pop("heartbeat_interval", UNSET)

        max_callback_backoff_delay_ms = d.pop("max_callback_backoff_delay_ms", UNSET)

        _media = d.pop("media", UNSET)
        media: Union[Unset, Media]
        if isinstance(_media, Unset):
            media = UNSET
        else:
            media = Media.from_dict(_media)

        on_call_pager = d.pop("on_call_pager", UNSET)

        pass_through = d.pop("pass_through", UNSET)

        sent_status = d.pop("sent_status", UNSET)

        unhealthy_interval = d.pop("unhealthy_interval", UNSET)

        _webhooks = d.pop("webhooks", UNSET)
        webhooks: Union[Unset, Webhooks]
        if isinstance(_webhooks, Unset):
            webhooks = UNSET
        else:
            webhooks = Webhooks.from_dict(_webhooks)

        update_application_settings_request_body = cls(
            callback_backoff_delay_ms=callback_backoff_delay_ms,
            callback_persist=callback_persist,
            heartbeat_interval=heartbeat_interval,
            max_callback_backoff_delay_ms=max_callback_backoff_delay_ms,
            media=media,
            on_call_pager=on_call_pager,
            pass_through=pass_through,
            sent_status=sent_status,
            unhealthy_interval=unhealthy_interval,
            webhooks=webhooks,
        )

        update_application_settings_request_body.additional_properties = d
        return update_application_settings_request_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
