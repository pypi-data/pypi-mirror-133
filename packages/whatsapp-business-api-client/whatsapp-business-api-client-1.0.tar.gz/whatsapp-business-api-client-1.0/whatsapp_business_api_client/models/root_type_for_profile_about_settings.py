from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.root_type_for_about_xxx import RootTypeForAboutXXX
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForProfileAboutSettings")


@attr.s(auto_attribs=True)
class RootTypeForProfileAboutSettings:
    """
    Example:
        {'profile': {'about': {'text': 'your-profile-about-text'}}}

    Attributes:
        profile (Union[Unset, RootTypeForAboutXXX]):  Example: {'about': {'text': 'your-profile-about-text'}}.
    """

    profile: Union[Unset, RootTypeForAboutXXX] = UNSET
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
        profile: Union[Unset, RootTypeForAboutXXX]
        if isinstance(_profile, Unset):
            profile = UNSET
        else:
            profile = RootTypeForAboutXXX.from_dict(_profile)

        root_type_for_profile_about_settings = cls(
            profile=profile,
        )

        root_type_for_profile_about_settings.additional_properties = d
        return root_type_for_profile_about_settings

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
