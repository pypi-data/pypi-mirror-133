from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.set_shards_request_shards import SetShardsRequestShards

T = TypeVar("T", bound="SetShardsRequest")


@attr.s(auto_attribs=True)
class SetShardsRequest:
    """
    Example:
        {'cc': '<Country Code>', 'phone_number': '<Phone Number>', 'pin': '<Two-Step PIN>', 'shards': 32}

    Attributes:
        cc (str):
        phone_number (str):
        pin (str):
        shards (SetShardsRequestShards):
    """

    cc: str
    phone_number: str
    pin: str
    shards: SetShardsRequestShards
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cc = self.cc
        phone_number = self.phone_number
        pin = self.pin
        shards = self.shards.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cc": cc,
                "phone_number": phone_number,
                "pin": pin,
                "shards": shards,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cc = d.pop("cc")

        phone_number = d.pop("phone_number")

        pin = d.pop("pin")

        shards = SetShardsRequestShards(d.pop("shards"))

        set_shards_request = cls(
            cc=cc,
            phone_number=phone_number,
            pin=pin,
            shards=shards,
        )

        set_shards_request.additional_properties = d
        return set_shards_request

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
