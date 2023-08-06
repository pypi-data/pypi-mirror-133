from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.root_type_for_business_settings_business import RootTypeForBusinessSettingsBusiness
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForBusinessSettings")


@attr.s(auto_attribs=True)
class RootTypeForBusinessSettings:
    """
    Example:
        {'business': {'profile': {'address': 'new-business-address', 'description': 'business-description', 'email':
            'new-business-email', 'vertical': 'business-industry', 'websites': ['website-1', 'website-2']}}}

    Attributes:
        business (Union[Unset, RootTypeForBusinessSettingsBusiness]):  Example: {'profile': {'address': 'new-business-
            address', 'description': 'business-description', 'email': 'new-business-email', 'vertical': 'business-industry',
            'websites': ['website-1', 'website-2']}}.
    """

    business: Union[Unset, RootTypeForBusinessSettingsBusiness] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        business: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.business, Unset):
            business = self.business.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if business is not UNSET:
            field_dict["business"] = business

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _business = d.pop("business", UNSET)
        business: Union[Unset, RootTypeForBusinessSettingsBusiness]
        if isinstance(_business, Unset):
            business = UNSET
        else:
            business = RootTypeForBusinessSettingsBusiness.from_dict(_business)

        root_type_for_business_settings = cls(
            business=business,
        )

        root_type_for_business_settings.additional_properties = d
        return root_type_for_business_settings

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
