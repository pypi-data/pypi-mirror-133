from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.user_role import UserRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForDetailedResponseItem")


@attr.s(auto_attribs=True)
class RootTypeForDetailedResponseItem:
    """
    Example:
        {'ROLES': 'ROLE_USER', 'username': 'username'}

    Attributes:
        roles (Union[Unset, UserRole]):
        username (Union[Unset, str]):
    """

    roles: Union[Unset, UserRole] = UNSET
    username: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        roles: Union[Unset, str] = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles.value

        username = self.username

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if roles is not UNSET:
            field_dict["ROLES"] = roles
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _roles = d.pop("ROLES", UNSET)
        roles: Union[Unset, UserRole]
        if isinstance(_roles, Unset):
            roles = UNSET
        else:
            roles = UserRole(_roles)

        username = d.pop("username", UNSET)

        root_type_for_detailed_response_item = cls(
            roles=roles,
            username=username,
        )

        root_type_for_detailed_response_item.additional_properties = d
        return root_type_for_detailed_response_item

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
