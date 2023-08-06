from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="RegisterAccountRequest")


@attr.s(auto_attribs=True)
class RegisterAccountRequest:
    """
    Example:
        {'code': 'your-registration-code-received-by-sms-or-voice-call'}

    Attributes:
        code (str):
    """

    code: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code")

        register_account_request = cls(
            code=code,
        )

        register_account_request.additional_properties = d
        return register_account_request

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
