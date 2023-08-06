from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForRequestCodeAccount")


@attr.s(auto_attribs=True)
class RootTypeForRequestCodeAccount:
    """
    Example:
        {'vname': 'decoded-vname-from-cert'}

    Attributes:
        vname (Union[Unset, str]):
    """

    vname: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        vname = self.vname

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if vname is not UNSET:
            field_dict["vname"] = vname

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        vname = d.pop("vname", UNSET)

        root_type_for_request_code_account = cls(
            vname=vname,
        )

        root_type_for_request_code_account.additional_properties = d
        return root_type_for_request_code_account

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
