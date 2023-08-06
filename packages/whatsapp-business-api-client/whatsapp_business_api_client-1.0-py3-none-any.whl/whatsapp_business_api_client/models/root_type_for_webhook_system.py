from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.root_type_for_webhook_system_type import RootTypeForWebhookSystemType
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForWebhookSystem")


@attr.s(auto_attribs=True)
class RootTypeForWebhookSystem:
    """
    Example:
        {'body': '+1 (650) 387-5246 added +1 (650) 644-8470', 'group_id': '16315558032-1530825318', 'operator':
            '16503875246', 'type': 'group_user_joined', 'users': ['16506448470']}

    Attributes:
        body (Union[Unset, str]):
        type (Union[Unset, RootTypeForWebhookSystemType]):
    """

    body: Union[Unset, str] = UNSET
    type: Union[Unset, RootTypeForWebhookSystemType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        body = self.body
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if body is not UNSET:
            field_dict["body"] = body
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        body = d.pop("body", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, RootTypeForWebhookSystemType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = RootTypeForWebhookSystemType(_type)

        root_type_for_webhook_system = cls(
            body=body,
            type=type,
        )

        root_type_for_webhook_system.additional_properties = d
        return root_type_for_webhook_system

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
