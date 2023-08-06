from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GroupResponseItem")


@attr.s(auto_attribs=True)
class GroupResponseItem:
    """
    Example:
        {'admins': ['whatsapp-id-1', 'whatsapp-id-2'], 'creation_time': 123456789, 'creator': 'whatsapp-id-1',
            'participants': ['whatsapp-id-3', 'whatsapp-id-4', 'whatsapp-id-5'], 'subject': 'your-group-subject'}

    Attributes:
        admins (Union[Unset, List[str]]): Group administrators
            Lists IDs of the creator of the group and any administrators added
        creation_time (Union[Unset, int]): Group creation time
        creator (Union[Unset, str]): ID of the creator of this group
        participants (Union[Unset, List[str]]): Participants of the group
            This is an array of all the IDs of the participants in the group. Initially, this will be the creator of the
            group.
        subject (Union[Unset, str]): Subject of the group
    """

    admins: Union[Unset, List[str]] = UNSET
    creation_time: Union[Unset, int] = UNSET
    creator: Union[Unset, str] = UNSET
    participants: Union[Unset, List[str]] = UNSET
    subject: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        admins: Union[Unset, List[str]] = UNSET
        if not isinstance(self.admins, Unset):
            admins = self.admins

        creation_time = self.creation_time
        creator = self.creator
        participants: Union[Unset, List[str]] = UNSET
        if not isinstance(self.participants, Unset):
            participants = self.participants

        subject = self.subject

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if admins is not UNSET:
            field_dict["admins"] = admins
        if creation_time is not UNSET:
            field_dict["creation_time"] = creation_time
        if creator is not UNSET:
            field_dict["creator"] = creator
        if participants is not UNSET:
            field_dict["participants"] = participants
        if subject is not UNSET:
            field_dict["subject"] = subject

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        admins = cast(List[str], d.pop("admins", UNSET))

        creation_time = d.pop("creation_time", UNSET)

        creator = d.pop("creator", UNSET)

        participants = cast(List[str], d.pop("participants", UNSET))

        subject = d.pop("subject", UNSET)

        group_response_item = cls(
            admins=admins,
            creation_time=creation_time,
            creator=creator,
            participants=participants,
            subject=subject,
        )

        group_response_item.additional_properties = d
        return group_response_item

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
