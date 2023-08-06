from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.webhooks_max_concurrent_requests import WebhooksMaxConcurrentRequests
from ..types import UNSET, Unset

T = TypeVar("T", bound="Webhooks")


@attr.s(auto_attribs=True)
class Webhooks:
    """
    Example:
        {'max_concurrent_requests': 12, 'url': '<Webhook URL, https>'}

    Attributes:
        max_concurrent_requests (Union[Unset, WebhooksMaxConcurrentRequests]): Configures the maximum number of inflight
            callback requests that are sent out. Can be set to 6 (default), 12, 18, or 24. Default:
            WebhooksMaxConcurrentRequests.VALUE_6.
        url (Union[Unset, str]): Inbound and outbound notifications are routed to this URL. A HTTPS-based endpoint is
            required; HTTP will not work.
    """

    max_concurrent_requests: Union[Unset, WebhooksMaxConcurrentRequests] = WebhooksMaxConcurrentRequests.VALUE_6
    url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        max_concurrent_requests: Union[Unset, int] = UNSET
        if not isinstance(self.max_concurrent_requests, Unset):
            max_concurrent_requests = self.max_concurrent_requests.value

        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_concurrent_requests is not UNSET:
            field_dict["max_concurrent_requests"] = max_concurrent_requests
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _max_concurrent_requests = d.pop("max_concurrent_requests", UNSET)
        max_concurrent_requests: Union[Unset, WebhooksMaxConcurrentRequests]
        if isinstance(_max_concurrent_requests, Unset):
            max_concurrent_requests = UNSET
        else:
            max_concurrent_requests = WebhooksMaxConcurrentRequests(_max_concurrent_requests)

        url = d.pop("url", UNSET)

        webhooks = cls(
            max_concurrent_requests=max_concurrent_requests,
            url=url,
        )

        webhooks.additional_properties = d
        return webhooks

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
