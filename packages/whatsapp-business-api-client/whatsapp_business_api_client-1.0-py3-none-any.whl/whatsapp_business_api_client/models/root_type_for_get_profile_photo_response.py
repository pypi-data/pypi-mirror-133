from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.root_type_for_profile_photo_settings import RootTypeForProfilePhotoSettings
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForGetProfilePhotoResponse")


@attr.s(auto_attribs=True)
class RootTypeForGetProfilePhotoResponse:
    """
    Example:
        {'settings': {'profile': {'photo': {'link': 'profile-photo-url'}}}}

    Attributes:
        settings (Union[Unset, RootTypeForProfilePhotoSettings]):  Example: {'profile': {'photo': {'link': 'profile-
            photo-url'}}}.
    """

    settings: Union[Unset, RootTypeForProfilePhotoSettings] = UNSET
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
        settings: Union[Unset, RootTypeForProfilePhotoSettings]
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = RootTypeForProfilePhotoSettings.from_dict(_settings)

        root_type_for_get_profile_photo_response = cls(
            settings=settings,
        )

        root_type_for_get_profile_photo_response.additional_properties = d
        return root_type_for_get_profile_photo_response

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
