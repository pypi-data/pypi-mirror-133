from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.error import Error
from ..models.group_response_item import GroupResponseItem
from ..models.meta import Meta
from ..types import UNSET, Unset

T = TypeVar("T", bound="GroupResponse")


@attr.s(auto_attribs=True)
class GroupResponse:
    """
    Example:
        {'groups': [{'admins': ['whatsapp-id-1', 'whatsapp-id-2'], 'creation_time': 123456789, 'creator': 'whatsapp-
            id-1', 'participants': ['whatsapp-id-3', 'whatsapp-id-4', 'whatsapp-id-5'], 'subject': 'your-group-subject'}]}

    Attributes:
        errors (Union[Unset, List[Error]]): Only returned with a failed request. Contains an array of error objects that
            are present when there is an error.
        meta (Union[Unset, Meta]): Contains generic information such as WhatsApp Business API Client version. Example:
            {'api_status': 'stable', 'version': 'whatsapp-business-api-client-version'}.
        groups (Union[Unset, List[GroupResponseItem]]):
    """

    errors: Union[Unset, List[Error]] = UNSET
    meta: Union[Unset, Meta] = UNSET
    groups: Union[Unset, List[GroupResponseItem]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        errors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for errors_item_data in self.errors:
                errors_item = errors_item_data.to_dict()

                errors.append(errors_item)

        meta: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        groups: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = []
            for groups_item_data in self.groups:
                groups_item = groups_item_data.to_dict()

                groups.append(groups_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if errors is not UNSET:
            field_dict["errors"] = errors
        if meta is not UNSET:
            field_dict["meta"] = meta
        if groups is not UNSET:
            field_dict["groups"] = groups

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        errors = []
        _errors = d.pop("errors", UNSET)
        for errors_item_data in _errors or []:
            errors_item = Error.from_dict(errors_item_data)

            errors.append(errors_item)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, Meta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = Meta.from_dict(_meta)

        groups = []
        _groups = d.pop("groups", UNSET)
        for groups_item_data in _groups or []:
            groups_item = GroupResponseItem.from_dict(groups_item_data)

            groups.append(groups_item)

        group_response = cls(
            errors=errors,
            meta=meta,
            groups=groups,
        )

        group_response.additional_properties = d
        return group_response

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
