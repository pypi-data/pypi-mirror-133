from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.root_type_for_gateway_node_status_role import RootTypeForGatewayNodeStatusRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForGatewayNodeStatus")


@attr.s(auto_attribs=True)
class RootTypeForGatewayNodeStatus:
    """
    Example:
        {'gateway_status': 'connected', 'role': 'coreapp'}

    Attributes:
        gateway_status (Union[Unset, str]):
        role (Union[Unset, RootTypeForGatewayNodeStatusRole]):
    """

    gateway_status: Union[Unset, str] = UNSET
    role: Union[Unset, RootTypeForGatewayNodeStatusRole] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        gateway_status = self.gateway_status
        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if gateway_status is not UNSET:
            field_dict["gateway_status"] = gateway_status
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        gateway_status = d.pop("gateway_status", UNSET)

        _role = d.pop("role", UNSET)
        role: Union[Unset, RootTypeForGatewayNodeStatusRole]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = RootTypeForGatewayNodeStatusRole(_role)

        root_type_for_gateway_node_status = cls(
            gateway_status=gateway_status,
            role=role,
        )

        root_type_for_gateway_node_status.additional_properties = d
        return root_type_for_gateway_node_status

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
