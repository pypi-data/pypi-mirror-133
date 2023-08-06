from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.error import Error
from ..models.root_type_for_webhook_status_status import RootTypeForWebhookStatusStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForWebhookStatus")


@attr.s(auto_attribs=True)
class RootTypeForWebhookStatus:
    """
    Example:
        {'errors': [{'code': 470, 'title': 'Failed to send message because you are outside the support window for
            freeform messages to this user. Please use a valid HSM notification or reconsider.'}], 'id':
            'gBGGEgZHMlEfAgkM1RBkhDRr7t8', 'recipient_id': '12064001000', 'status': 'failed', 'timestamp': '1533332775'}

    Attributes:
        errors (Union[Unset, List[Error]]):
        id (Union[Unset, str]): Message ID
        recipient_id (Union[Unset, str]): WhatsApp ID of recipient
        status (Union[Unset, RootTypeForWebhookStatusStatus]): Status of message
        timestamp (Union[Unset, str]): Timestamp of the status message
    """

    errors: Union[Unset, List[Error]] = UNSET
    id: Union[Unset, str] = UNSET
    recipient_id: Union[Unset, str] = UNSET
    status: Union[Unset, RootTypeForWebhookStatusStatus] = UNSET
    timestamp: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        errors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for errors_item_data in self.errors:
                errors_item = errors_item_data.to_dict()

                errors.append(errors_item)

        id = self.id
        recipient_id = self.recipient_id
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        timestamp = self.timestamp

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if errors is not UNSET:
            field_dict["errors"] = errors
        if id is not UNSET:
            field_dict["id"] = id
        if recipient_id is not UNSET:
            field_dict["recipient_id"] = recipient_id
        if status is not UNSET:
            field_dict["status"] = status
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        errors = []
        _errors = d.pop("errors", UNSET)
        for errors_item_data in _errors or []:
            errors_item = Error.from_dict(errors_item_data)

            errors.append(errors_item)

        id = d.pop("id", UNSET)

        recipient_id = d.pop("recipient_id", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, RootTypeForWebhookStatusStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = RootTypeForWebhookStatusStatus(_status)

        timestamp = d.pop("timestamp", UNSET)

        root_type_for_webhook_status = cls(
            errors=errors,
            id=id,
            recipient_id=recipient_id,
            status=status,
            timestamp=timestamp,
        )

        root_type_for_webhook_status.additional_properties = d
        return root_type_for_webhook_status

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
