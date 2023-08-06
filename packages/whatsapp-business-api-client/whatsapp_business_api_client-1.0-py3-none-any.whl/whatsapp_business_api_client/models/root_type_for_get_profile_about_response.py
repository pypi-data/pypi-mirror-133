from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.root_type_for_profile_about_settings import RootTypeForProfileAboutSettings
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForGetProfileAboutResponse")


@attr.s(auto_attribs=True)
class RootTypeForGetProfileAboutResponse:
    """
    Example:
        {'settings': {'profile': {'about': {'text': 'your-profile-about-text'}}}}

    Attributes:
        settings (Union[Unset, RootTypeForProfileAboutSettings]):  Example: {'profile': {'about': {'text': 'your-
            profile-about-text'}}}.
    """

    settings: Union[Unset, RootTypeForProfileAboutSettings] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if settings is not UNSET:
            field_dict["settings"] = settings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, RootTypeForProfileAboutSettings]
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = RootTypeForProfileAboutSettings.from_dict(_settings)

        root_type_for_get_profile_about_response = cls(
            settings=settings,
        )

        root_type_for_get_profile_about_response.additional_properties = d
        return root_type_for_get_profile_about_response

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
