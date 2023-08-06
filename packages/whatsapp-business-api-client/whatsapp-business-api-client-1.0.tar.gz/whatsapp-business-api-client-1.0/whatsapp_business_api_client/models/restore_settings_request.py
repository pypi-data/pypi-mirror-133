from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="RestoreSettingsRequest")


@attr.s(auto_attribs=True)
class RestoreSettingsRequest:
    """
    Example:
        {'data': '<Data to Restore, from Backup API>', 'password': '<Password for Backup>'}

    Attributes:
        data (str): The data that was returned by the /v1/settings/backup API call
        password (str): The password you used in the /v1/settings/backup API call to encrypt the backup data
    """

    data: str
    password: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = self.data
        password = self.password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "password": password,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data = d.pop("data")

        password = d.pop("password")

        restore_settings_request = cls(
            data=data,
            password=password,
        )

        restore_settings_request.additional_properties = d
        return restore_settings_request

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
