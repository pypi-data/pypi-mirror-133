from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Error")


@attr.s(auto_attribs=True)
class Error:
    """
    Example:
        {'code': 1234, 'details': 'optional-detailed-error-message', 'title': 'error-code-title'}

    Attributes:
        code (Union[Unset, int]): See the https://developers.facebook.com/docs/whatsapp/api/errors for more information.
        details (Union[Unset, str]): error detail
        href (Union[Unset, str]): location for error detail
        title (Union[Unset, str]): error title
    """

    code: Union[Unset, int] = UNSET
    details: Union[Unset, str] = UNSET
    href: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        details = self.details
        href = self.href
        title = self.title

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if details is not UNSET:
            field_dict["details"] = details
        if href is not UNSET:
            field_dict["href"] = href
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code", UNSET)

        details = d.pop("details", UNSET)

        href = d.pop("href", UNSET)

        title = d.pop("title", UNSET)

        error = cls(
            code=code,
            details=details,
            href=href,
            title=title,
        )

        error.additional_properties = d
        return error

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
