from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.check_contact import CheckContact
from ..models.error import Error
from ..models.meta import Meta
from ..types import UNSET, Unset

T = TypeVar("T", bound="CheckContactResponse")


@attr.s(auto_attribs=True)
class CheckContactResponse:
    """
    Example:
        {'contacts': [{'input': '1-631-555-1002', 'status': 'processing'}, {'input': '6315551003', 'status':
            'processing'}, {'input': '+54 9 11 5612-1008', 'status': 'processing'}, {'input': '+1 (516) 283-7151', 'status':
            'valid', 'wa_id': '15162837151'}]}

    Attributes:
        errors (Union[Unset, List[Error]]): Only returned with a failed request. Contains an array of error objects that
            are present when there is an error.
        meta (Union[Unset, Meta]): Contains generic information such as WhatsApp Business API Client version. Example:
            {'api_status': 'stable', 'version': 'whatsapp-business-api-client-version'}.
        contacts (Union[Unset, List[CheckContact]]):
    """

    errors: Union[Unset, List[Error]] = UNSET
    meta: Union[Unset, Meta] = UNSET
    contacts: Union[Unset, List[CheckContact]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        errors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for errors_item_data in self.errors:
                errors_item = errors_item_data.to_dict()

                errors.append(errors_item)

        meta: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        contacts: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.contacts, Unset):
            contacts = []
            for contacts_item_data in self.contacts:
                contacts_item = contacts_item_data.to_dict()

                contacts.append(contacts_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if errors is not UNSET:
            field_dict["errors"] = errors
        if meta is not UNSET:
            field_dict["meta"] = meta
        if contacts is not UNSET:
            field_dict["contacts"] = contacts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        errors = []
        _errors = d.pop("errors", UNSET)
        for errors_item_data in _errors or []:
            errors_item = Error.from_dict(errors_item_data)

            errors.append(errors_item)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, Meta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = Meta.from_dict(_meta)

        contacts = []
        _contacts = d.pop("contacts", UNSET)
        for contacts_item_data in _contacts or []:
            contacts_item = CheckContact.from_dict(contacts_item_data)

            contacts.append(contacts_item)

        check_contact_response = cls(
            errors=errors,
            meta=meta,
            contacts=contacts,
        )

        check_contact_response.additional_properties = d
        return check_contact_response

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
