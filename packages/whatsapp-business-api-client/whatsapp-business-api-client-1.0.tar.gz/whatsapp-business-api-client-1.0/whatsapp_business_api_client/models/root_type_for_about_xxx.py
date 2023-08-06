from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.set_profile_about_request import SetProfileAboutRequest
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForAboutXXX")


@attr.s(auto_attribs=True)
class RootTypeForAboutXXX:
    """
    Example:
        {'about': {'text': 'your-profile-about-text'}}

    Attributes:
        about (Union[Unset, SetProfileAboutRequest]):  Example: {'text': '<About Profile>'}.
    """

    about: Union[Unset, SetProfileAboutRequest] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        about: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.about, Unset):
            about = self.about.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if about is not UNSET:
            field_dict["about"] = about

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _about = d.pop("about", UNSET)
        about: Union[Unset, SetProfileAboutRequest]
        if isinstance(_about, Unset):
            about = UNSET
        else:
            about = SetProfileAboutRequest.from_dict(_about)

        root_type_for_about_xxx = cls(
            about=about,
        )

        root_type_for_about_xxx.additional_properties = d
        return root_type_for_about_xxx

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
