from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="LoginAdminRequest")


@attr.s(auto_attribs=True)
class LoginAdminRequest:
    """
    Example:
        {'new_password': '<New Admin Password>'}

    Attributes:
        new_password (str):
    """

    new_password: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        new_password = self.new_password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "new_password": new_password,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        new_password = d.pop("new_password")

        login_admin_request = cls(
            new_password=new_password,
        )

        login_admin_request.additional_properties = d
        return login_admin_request

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
