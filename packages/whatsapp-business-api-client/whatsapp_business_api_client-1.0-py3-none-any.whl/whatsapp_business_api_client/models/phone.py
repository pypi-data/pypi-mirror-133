from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Phone")


@attr.s(auto_attribs=True)
class Phone:
    """
    Example:
        {'phone': '+1 (650) 555-1234', 'type': 'WORK', 'wa_id': '16505551234'}

    Attributes:
        phone (Union[Unset, str]):
        type (Union[Unset, str]): Standard Values: CELL, MAIN, IPHONE, HOME, WORK
        wa_id (Union[Unset, str]): WhatsApp ID
    """

    phone: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    wa_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        phone = self.phone
        type = self.type
        wa_id = self.wa_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if phone is not UNSET:
            field_dict["phone"] = phone
        if type is not UNSET:
            field_dict["type"] = type
        if wa_id is not UNSET:
            field_dict["wa_id"] = wa_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        phone = d.pop("phone", UNSET)

        type = d.pop("type", UNSET)

        wa_id = d.pop("wa_id", UNSET)

        phone = cls(
            phone=phone,
            type=type,
            wa_id=wa_id,
        )

        phone.additional_properties = d
        return phone

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
