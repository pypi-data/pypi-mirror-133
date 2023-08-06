from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Org")


@attr.s(auto_attribs=True)
class Org:
    """Contact organization information

    Example:
        {'company': 'WhatsApp', 'department': 'Design', 'title': 'Manager'}

    Attributes:
        company (str): Name of the contact's company
        department (Union[Unset, str]): Name of the contact's department
        title (Union[Unset, str]): Contact's business title
    """

    company: str
    department: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        company = self.company
        department = self.department
        title = self.title

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "company": company,
            }
        )
        if department is not UNSET:
            field_dict["department"] = department
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        company = d.pop("company")

        department = d.pop("department", UNSET)

        title = d.pop("title", UNSET)

        org = cls(
            company=company,
            department=department,
            title=title,
        )

        org.additional_properties = d
        return org

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
