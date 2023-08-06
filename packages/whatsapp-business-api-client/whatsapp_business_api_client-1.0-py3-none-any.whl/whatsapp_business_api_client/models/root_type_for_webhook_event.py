from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.error import Error
from ..models.root_type_for_webhook_contact import RootTypeForWebhookContact
from ..models.root_type_for_webhook_message import RootTypeForWebhookMessage
from ..models.root_type_for_webhook_status import RootTypeForWebhookStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForWebhookEvent")


@attr.s(auto_attribs=True)
class RootTypeForWebhookEvent:
    """
    Example:
        {'contacts': [{'profile': {'name': 'Kerry Fisher'}, 'wa_id': '16315551234'}], 'messages': [{'from':
            '16315551234', 'id': 'ABGGFlA5FpafAgo6tHcNmNjXmuSf', 'text': {'body': 'Hello this is an answer'}, 'timestamp':
            '1518694235', 'type': 'text'}]}

    Attributes:
        contacts (Union[Unset, List[RootTypeForWebhookContact]]):
        errors (Union[Unset, List[Error]]):
        messages (Union[Unset, List[RootTypeForWebhookMessage]]):
        statuses (Union[Unset, List[RootTypeForWebhookStatus]]):
    """

    contacts: Union[Unset, List[RootTypeForWebhookContact]] = UNSET
    errors: Union[Unset, List[Error]] = UNSET
    messages: Union[Unset, List[RootTypeForWebhookMessage]] = UNSET
    statuses: Union[Unset, List[RootTypeForWebhookStatus]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        contacts: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.contacts, Unset):
            contacts = []
            for contacts_item_data in self.contacts:
                contacts_item = contacts_item_data.to_dict()

                contacts.append(contacts_item)

        errors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for errors_item_data in self.errors:
                errors_item = errors_item_data.to_dict()

                errors.append(errors_item)

        messages: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.messages, Unset):
            messages = []
            for messages_item_data in self.messages:
                messages_item = messages_item_data.to_dict()

                messages.append(messages_item)

        statuses: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.statuses, Unset):
            statuses = []
            for statuses_item_data in self.statuses:
                statuses_item = statuses_item_data.to_dict()

                statuses.append(statuses_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if contacts is not UNSET:
            field_dict["contacts"] = contacts
        if errors is not UNSET:
            field_dict["errors"] = errors
        if messages is not UNSET:
            field_dict["messages"] = messages
        if statuses is not UNSET:
            field_dict["statuses"] = statuses

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        contacts = []
        _contacts = d.pop("contacts", UNSET)
        for contacts_item_data in _contacts or []:
            contacts_item = RootTypeForWebhookContact.from_dict(contacts_item_data)

            contacts.append(contacts_item)

        errors = []
        _errors = d.pop("errors", UNSET)
        for errors_item_data in _errors or []:
            errors_item = Error.from_dict(errors_item_data)

            errors.append(errors_item)

        messages = []
        _messages = d.pop("messages", UNSET)
        for messages_item_data in _messages or []:
            messages_item = RootTypeForWebhookMessage.from_dict(messages_item_data)

            messages.append(messages_item)

        statuses = []
        _statuses = d.pop("statuses", UNSET)
        for statuses_item_data in _statuses or []:
            statuses_item = RootTypeForWebhookStatus.from_dict(statuses_item_data)

            statuses.append(statuses_item)

        root_type_for_webhook_event = cls(
            contacts=contacts,
            errors=errors,
            messages=messages,
            statuses=statuses,
        )

        root_type_for_webhook_event.additional_properties = d
        return root_type_for_webhook_event

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
