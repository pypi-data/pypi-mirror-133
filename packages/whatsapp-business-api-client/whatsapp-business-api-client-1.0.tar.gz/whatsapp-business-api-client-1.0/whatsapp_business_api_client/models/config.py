from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.root_type_for_basic import RootTypeForBasic
from ..types import UNSET, Unset

T = TypeVar("T", bound="Config")


@attr.s(auto_attribs=True)
class Config:
    """
    Example:
        {'basic': {'password': 'your-password', 'username': 'your-username'}}

    Attributes:
        basic (Union[Unset, RootTypeForBasic]):  Example: {'password': 'your-password', 'username': 'your-username'}.
    """

    basic: Union[Unset, RootTypeForBasic] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        basic: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.basic, Unset):
            basic = self.basic.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if basic is not UNSET:
            field_dict["basic"] = basic

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _basic = d.pop("basic", UNSET)
        basic: Union[Unset, RootTypeForBasic]
        if isinstance(_basic, Unset):
            basic = UNSET
        else:
            basic = RootTypeForBasic.from_dict(_basic)

        config = cls(
            basic=basic,
        )

        config.additional_properties = d
        return config

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
