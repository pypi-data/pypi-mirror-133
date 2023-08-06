from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Name")


@attr.s(auto_attribs=True)
class Name:
    """Full contact name

    Example:
        {'first_name': 'John', 'formatted_name': 'John Smith', 'last_name': 'Smith'}

    Attributes:
        formatted_name (str): Full name as it normally appears
        first_name (Union[Unset, str]): First name
        last_name (Union[Unset, str]): Last name
        prefix (Union[Unset, str]): Name preffix
        suffix (Union[Unset, str]): Name suffix
    """

    formatted_name: str
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    prefix: Union[Unset, str] = UNSET
    suffix: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        formatted_name = self.formatted_name
        first_name = self.first_name
        last_name = self.last_name
        prefix = self.prefix
        suffix = self.suffix

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "formatted_name": formatted_name,
            }
        )
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if prefix is not UNSET:
            field_dict["prefix"] = prefix
        if suffix is not UNSET:
            field_dict["suffix"] = suffix

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        formatted_name = d.pop("formatted_name")

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        prefix = d.pop("prefix", UNSET)

        suffix = d.pop("suffix", UNSET)

        name = cls(
            formatted_name=formatted_name,
            first_name=first_name,
            last_name=last_name,
            prefix=prefix,
            suffix=suffix,
        )

        name.additional_properties = d
        return name

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
