from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.check_contact_status import CheckContactStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="CheckContact")


@attr.s(auto_attribs=True)
class CheckContact:
    """
    Example:
        {'input': '+1 (516) 283-7151', 'status': 'valid', 'wa_id': '15162837151'}

    Attributes:
        input_ (Union[Unset, str]): The value you sent in the contacts field of the JSON request.
        status (Union[Unset, CheckContactStatus]): Status of the user.
        wa_id (Union[Unset, str]): WhatsApp user identifier that can be used in other API calls. Only returned if the
            status is valid.
    """

    input_: Union[Unset, str] = UNSET
    status: Union[Unset, CheckContactStatus] = UNSET
    wa_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_ = self.input_
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        wa_id = self.wa_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if input_ is not UNSET:
            field_dict["input"] = input_
        if status is not UNSET:
            field_dict["status"] = status
        if wa_id is not UNSET:
            field_dict["wa_id"] = wa_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        input_ = d.pop("input", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, CheckContactStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = CheckContactStatus(_status)

        wa_id = d.pop("wa_id", UNSET)

        check_contact = cls(
            input_=input_,
            status=status,
            wa_id=wa_id,
        )

        check_contact.additional_properties = d
        return check_contact

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
