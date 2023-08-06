from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForMessageContext")


@attr.s(auto_attribs=True)
class RootTypeForMessageContext:
    """
    Example:
        {'from': 'sender-wa-id-of-context-message', 'group_id': 'group-id-of-context-message', 'id': 'message-id-of-
            context-message', 'mentions': ['wa-id1', 'wa-id2']}

    Attributes:
        from_ (Union[Unset, str]): Sender Whatsapp id of context-message
        group_id (Union[Unset, str]): GroupId of context message
        id (Union[Unset, str]): message id
        mentions (Union[Unset, List[str]]): Whats app ids
    """

    from_: Union[Unset, str] = UNSET
    group_id: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    mentions: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from_ = self.from_
        group_id = self.group_id
        id = self.id
        mentions: Union[Unset, List[str]] = UNSET
        if not isinstance(self.mentions, Unset):
            mentions = self.mentions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if from_ is not UNSET:
            field_dict["from"] = from_
        if group_id is not UNSET:
            field_dict["group_id"] = group_id
        if id is not UNSET:
            field_dict["id"] = id
        if mentions is not UNSET:
            field_dict["mentions"] = mentions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        from_ = d.pop("from", UNSET)

        group_id = d.pop("group_id", UNSET)

        id = d.pop("id", UNSET)

        mentions = cast(List[str], d.pop("mentions", UNSET))

        root_type_for_message_context = cls(
            from_=from_,
            group_id=group_id,
            id=id,
            mentions=mentions,
        )

        root_type_for_message_context.additional_properties = d
        return root_type_for_message_context

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
