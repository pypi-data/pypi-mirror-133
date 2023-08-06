from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="EnableTwoStepRequest")


@attr.s(auto_attribs=True)
class EnableTwoStepRequest:
    """
    Example:
        {'pin': 'your-6-digit-pin'}

    Attributes:
        pin (str):
    """

    pin: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pin = self.pin

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pin": pin,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pin = d.pop("pin")

        enable_two_step_request = cls(
            pin=pin,
        )

        enable_two_step_request.additional_properties = d
        return enable_two_step_request

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
