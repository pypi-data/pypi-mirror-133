from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="RemoveGroupParticipantRequest")


@attr.s(auto_attribs=True)
class RemoveGroupParticipantRequest:
    """
    Example:
        {'wa_ids': ['{{Recipient-WA-ID}}']}

    Attributes:
        wa_ids (List[str]):
    """

    wa_ids: List[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        wa_ids = self.wa_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "wa_ids": wa_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        wa_ids = cast(List[str], d.pop("wa_ids"))

        remove_group_participant_request = cls(
            wa_ids=wa_ids,
        )

        remove_group_participant_request.additional_properties = d
        return remove_group_participant_request

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
