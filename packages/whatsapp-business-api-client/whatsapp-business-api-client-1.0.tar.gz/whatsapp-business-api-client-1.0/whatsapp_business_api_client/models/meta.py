from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.meta_api_status import MetaApiStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="Meta")


@attr.s(auto_attribs=True)
class Meta:
    """Contains generic information such as WhatsApp Business API Client version.

    Example:
        {'api_status': 'stable', 'version': 'whatsapp-business-api-client-version'}

    Attributes:
        api_status (Union[Unset, MetaApiStatus]):
        version (Union[Unset, str]):
    """

    api_status: Union[Unset, MetaApiStatus] = UNSET
    version: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        api_status: Union[Unset, str] = UNSET
        if not isinstance(self.api_status, Unset):
            api_status = self.api_status.value

        version = self.version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if api_status is not UNSET:
            field_dict["api_status"] = api_status
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _api_status = d.pop("api_status", UNSET)
        api_status: Union[Unset, MetaApiStatus]
        if isinstance(_api_status, Unset):
            api_status = UNSET
        else:
            api_status = MetaApiStatus(_api_status)

        version = d.pop("version", UNSET)

        meta = cls(
            api_status=api_status,
            version=version,
        )

        meta.additional_properties = d
        return meta

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
