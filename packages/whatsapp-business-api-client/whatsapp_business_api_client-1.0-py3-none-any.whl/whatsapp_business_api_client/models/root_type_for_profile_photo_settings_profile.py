from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.root_type_for_profile_photo_settings_profile_photo import RootTypeForProfilePhotoSettingsProfilePhoto
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForProfilePhotoSettingsProfile")


@attr.s(auto_attribs=True)
class RootTypeForProfilePhotoSettingsProfile:
    """
    Example:
        {'photo': {'link': 'profile-photo-url'}}

    Attributes:
        photo (Union[Unset, RootTypeForProfilePhotoSettingsProfilePhoto]):  Example: {'link': 'profile-photo-url'}.
    """

    photo: Union[Unset, RootTypeForProfilePhotoSettingsProfilePhoto] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        photo: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.photo, Unset):
            photo = self.photo.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if photo is not UNSET:
            field_dict["photo"] = photo

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _photo = d.pop("photo", UNSET)
        photo: Union[Unset, RootTypeForProfilePhotoSettingsProfilePhoto]
        if isinstance(_photo, Unset):
            photo = UNSET
        else:
            photo = RootTypeForProfilePhotoSettingsProfilePhoto.from_dict(_photo)

        root_type_for_profile_photo_settings_profile = cls(
            photo=photo,
        )

        root_type_for_profile_photo_settings_profile.additional_properties = d
        return root_type_for_profile_photo_settings_profile

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
