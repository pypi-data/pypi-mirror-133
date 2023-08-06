from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.gateway_status import GatewayStatus
from ..models.root_type_for_check_health_response_health_type_1 import RootTypeForCheckHealthResponseHealthType1
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForCheckHealthResponse")


@attr.s(auto_attribs=True)
class RootTypeForCheckHealthResponse:
    """
    Example:
        {'health': {'your-hostname1:your-container-id1': {'gateway_status': 'connected', 'role': 'primary_master'},
            'your-hostname2:your-container-id2': {'gateway_status': 'disconnected', 'role': 'secondary_master'}}}

    Attributes:
        health (Union[GatewayStatus, RootTypeForCheckHealthResponseHealthType1, Unset]):
    """

    health: Union[GatewayStatus, RootTypeForCheckHealthResponseHealthType1, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        health: Union[Dict[str, Any], Unset, str]
        if isinstance(self.health, Unset):
            health = UNSET
        elif isinstance(self.health, GatewayStatus):
            health = UNSET
            if not isinstance(self.health, Unset):
                health = self.health.value

        else:
            health = UNSET
            if not isinstance(self.health, Unset):
                health = self.health.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if health is not UNSET:
            field_dict["health"] = health

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_health(data: object) -> Union[GatewayStatus, RootTypeForCheckHealthResponseHealthType1, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                _health_type_0 = data
                health_type_0: Union[Unset, GatewayStatus]
                if isinstance(_health_type_0, Unset):
                    health_type_0 = UNSET
                else:
                    health_type_0 = GatewayStatus(_health_type_0)

                return health_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _health_type_1 = data
            health_type_1: Union[Unset, RootTypeForCheckHealthResponseHealthType1]
            if isinstance(_health_type_1, Unset):
                health_type_1 = UNSET
            else:
                health_type_1 = RootTypeForCheckHealthResponseHealthType1.from_dict(_health_type_1)

            return health_type_1

        health = _parse_health(d.pop("health", UNSET))

        root_type_for_check_health_response = cls(
            health=health,
        )

        root_type_for_check_health_response.additional_properties = d
        return root_type_for_check_health_response

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
