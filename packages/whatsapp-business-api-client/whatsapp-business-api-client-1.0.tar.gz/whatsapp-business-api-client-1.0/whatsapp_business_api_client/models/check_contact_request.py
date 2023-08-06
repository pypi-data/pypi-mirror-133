from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.check_contact_request_blocking import CheckContactRequestBlocking
from ..types import UNSET, Unset

T = TypeVar("T", bound="CheckContactRequest")


@attr.s(auto_attribs=True)
class CheckContactRequest:
    """
    Example:
        {'blocking': 'wait', 'contacts': ['{{Recipient-WA-ID}}']}

    Attributes:
        contacts (List[str]): Array of contact phone numbers. The numbers can be in any standard telephone number
            format.
        blocking (Union[Unset, CheckContactRequestBlocking]): Blocking determines whether the request should wait for
            the processing to complete (synchronous) or not (asynchronous). Default: CheckContactRequestBlocking.NO_WAIT.
    """

    contacts: List[str]
    blocking: Union[Unset, CheckContactRequestBlocking] = CheckContactRequestBlocking.NO_WAIT
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        contacts = self.contacts

        blocking: Union[Unset, str] = UNSET
        if not isinstance(self.blocking, Unset):
            blocking = self.blocking.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "contacts": contacts,
            }
        )
        if blocking is not UNSET:
            field_dict["blocking"] = blocking

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        contacts = cast(List[str], d.pop("contacts"))

        _blocking = d.pop("blocking", UNSET)
        blocking: Union[Unset, CheckContactRequestBlocking]
        if isinstance(_blocking, Unset):
            blocking = UNSET
        else:
            blocking = CheckContactRequestBlocking(_blocking)

        check_contact_request = cls(
            contacts=contacts,
            blocking=blocking,
        )

        check_contact_request.additional_properties = d
        return check_contact_request

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
