from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.set_business_profile_request import SetBusinessProfileRequest
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForBusinessSettingsBusiness")


@attr.s(auto_attribs=True)
class RootTypeForBusinessSettingsBusiness:
    """
    Example:
        {'profile': {'address': 'new-business-address', 'description': 'business-description', 'email': 'new-business-
            email', 'vertical': 'business-industry', 'websites': ['website-1', 'website-2']}}

    Attributes:
        profile (Union[Unset, SetBusinessProfileRequest]):  Example: {'address': '<Business Profile Address>',
            'description': '<Business Profile Description>', 'email': '<Business Profile Email>', 'vertical': '<Business
            Profile Vertical>', 'websites': ['https://www.whatsapp.com', 'https://www.facebook.com']}.
    """

    profile: Union[Unset, SetBusinessProfileRequest] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        profile: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.profile, Unset):
            profile = self.profile.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if profile is not UNSET:
            field_dict["profile"] = profile

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _profile = d.pop("profile", UNSET)
        profile: Union[Unset, SetBusinessProfileRequest]
        if isinstance(_profile, Unset):
            profile = UNSET
        else:
            profile = SetBusinessProfileRequest.from_dict(_profile)

        root_type_for_business_settings_business = cls(
            profile=profile,
        )

        root_type_for_business_settings_business.additional_properties = d
        return root_type_for_business_settings_business

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
