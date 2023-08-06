from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.root_type_for_backup_settings import RootTypeForBackupSettings
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForBackupSettingsResponse")


@attr.s(auto_attribs=True)
class RootTypeForBackupSettingsResponse:
    """Save the data value as that will be used along with your password to restore the information.

    Example:
        {'settings': {'data': 'encrypted-backup-data'}}

    Attributes:
        settings (Union[Unset, RootTypeForBackupSettings]):  Example: {'data': 'encrypted-backup-data'}.
    """

    settings: Union[Unset, RootTypeForBackupSettings] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if settings is not UNSET:
            field_dict["settings"] = settings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, RootTypeForBackupSettings]
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = RootTypeForBackupSettings.from_dict(_settings)

        root_type_for_backup_settings_response = cls(
            settings=settings,
        )

        root_type_for_backup_settings_response.additional_properties = d
        return root_type_for_backup_settings_response

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
