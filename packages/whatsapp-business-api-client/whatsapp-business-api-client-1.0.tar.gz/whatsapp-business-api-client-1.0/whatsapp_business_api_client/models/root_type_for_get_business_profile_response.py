from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.error import Error
from ..models.meta import Meta
from ..models.root_type_for_business_settings import RootTypeForBusinessSettings
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForGetBusinessProfileResponse")


@attr.s(auto_attribs=True)
class RootTypeForGetBusinessProfileResponse:
    """
    Example:
        {'settings': {'business': {'profile': {'address': 'new-business-address', 'description': 'business-description',
            'email': 'new-business-email', 'vertical': 'business-industry', 'websites': ['website-1', 'website-2']}}}}

    Attributes:
        errors (Union[Unset, List[Error]]): Only returned with a failed request. Contains an array of error objects that
            are present when there is an error.
        meta (Union[Unset, Meta]): Contains generic information such as WhatsApp Business API Client version. Example:
            {'api_status': 'stable', 'version': 'whatsapp-business-api-client-version'}.
        settings (Union[Unset, RootTypeForBusinessSettings]):  Example: {'business': {'profile': {'address': 'new-
            business-address', 'description': 'business-description', 'email': 'new-business-email', 'vertical': 'business-
            industry', 'websites': ['website-1', 'website-2']}}}.
    """

    errors: Union[Unset, List[Error]] = UNSET
    meta: Union[Unset, Meta] = UNSET
    settings: Union[Unset, RootTypeForBusinessSettings] = UNSET
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

        settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if errors is not UNSET:
            field_dict["errors"] = errors
        if meta is not UNSET:
            field_dict["meta"] = meta
        if settings is not UNSET:
            field_dict["settings"] = settings

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

        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, RootTypeForBusinessSettings]
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = RootTypeForBusinessSettings.from_dict(_settings)

        root_type_for_get_business_profile_response = cls(
            errors=errors,
            meta=meta,
            settings=settings,
        )

        root_type_for_get_business_profile_response.additional_properties = d
        return root_type_for_get_business_profile_response

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
