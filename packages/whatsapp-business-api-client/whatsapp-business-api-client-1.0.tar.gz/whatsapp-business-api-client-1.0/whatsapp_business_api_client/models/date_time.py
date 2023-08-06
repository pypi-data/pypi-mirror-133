from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.date_time_component import DateTimeComponent
from ..models.date_time_unix_epoch import DateTimeUnixEpoch
from ..types import UNSET, Unset

T = TypeVar("T", bound="DateTime")


@attr.s(auto_attribs=True)
class DateTime:
    """The Whatsapp Business API Client will attempt to format the date/time based on a specified localization.

    Example:
        {'component': {'day_of_month': 25, 'day_of_week': 5, 'hour': 15, 'minute': 33, 'month': 2, 'year': 1977}}

    Attributes:
        component (Union[Unset, DateTimeComponent]): Date/time by component Example: {'day_of_month': 25, 'day_of_week':
            5, 'hour': 15, 'minute': 33, 'month': 2, 'year': 1977}.
        unix_epoch (Union[Unset, DateTimeUnixEpoch]): Date/time by Unix epoch Example: {'timestamp': 123456789}.
    """

    component: Union[Unset, DateTimeComponent] = UNSET
    unix_epoch: Union[Unset, DateTimeUnixEpoch] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        component: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.component, Unset):
            component = self.component.to_dict()

        unix_epoch: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.unix_epoch, Unset):
            unix_epoch = self.unix_epoch.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if component is not UNSET:
            field_dict["component"] = component
        if unix_epoch is not UNSET:
            field_dict["unix_epoch"] = unix_epoch

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _component = d.pop("component", UNSET)
        component: Union[Unset, DateTimeComponent]
        if isinstance(_component, Unset):
            component = UNSET
        else:
            component = DateTimeComponent.from_dict(_component)

        _unix_epoch = d.pop("unix_epoch", UNSET)
        unix_epoch: Union[Unset, DateTimeUnixEpoch]
        if isinstance(_unix_epoch, Unset):
            unix_epoch = UNSET
        else:
            unix_epoch = DateTimeUnixEpoch.from_dict(_unix_epoch)

        date_time = cls(
            component=component,
            unix_epoch=unix_epoch,
        )

        date_time.additional_properties = d
        return date_time

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
