from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.date_time_component_day_of_week import DateTimeComponentDayOfWeek
from ..types import UNSET, Unset

T = TypeVar("T", bound="DateTimeComponent")


@attr.s(auto_attribs=True)
class DateTimeComponent:
    """Date/time by component

    Example:
        {'day_of_month': 25, 'day_of_week': 5, 'hour': 15, 'minute': 33, 'month': 2, 'year': 1977}

    Attributes:
        day_of_month (Union[Unset, int]): The day of month
        day_of_week (Union[Unset, DateTimeComponentDayOfWeek]): Both strings and numbers are accepted. If different from
            the value derived from the date (if specified), use the derived value.
        hour (Union[Unset, int]): The hour
        minute (Union[Unset, int]): The minute
        month (Union[Unset, int]): The month
        year (Union[Unset, int]): The year
    """

    day_of_month: Union[Unset, int] = UNSET
    day_of_week: Union[Unset, DateTimeComponentDayOfWeek] = UNSET
    hour: Union[Unset, int] = UNSET
    minute: Union[Unset, int] = UNSET
    month: Union[Unset, int] = UNSET
    year: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        day_of_month = self.day_of_month
        day_of_week: Union[Unset, int] = UNSET
        if not isinstance(self.day_of_week, Unset):
            day_of_week = self.day_of_week.value

        hour = self.hour
        minute = self.minute
        month = self.month
        year = self.year

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if day_of_month is not UNSET:
            field_dict["day_of_month"] = day_of_month
        if day_of_week is not UNSET:
            field_dict["day_of_week"] = day_of_week
        if hour is not UNSET:
            field_dict["hour"] = hour
        if minute is not UNSET:
            field_dict["minute"] = minute
        if month is not UNSET:
            field_dict["month"] = month
        if year is not UNSET:
            field_dict["year"] = year

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        day_of_month = d.pop("day_of_month", UNSET)

        _day_of_week = d.pop("day_of_week", UNSET)
        day_of_week: Union[Unset, DateTimeComponentDayOfWeek]
        if isinstance(_day_of_week, Unset):
            day_of_week = UNSET
        else:
            day_of_week = DateTimeComponentDayOfWeek(_day_of_week)

        hour = d.pop("hour", UNSET)

        minute = d.pop("minute", UNSET)

        month = d.pop("month", UNSET)

        year = d.pop("year", UNSET)

        date_time_component = cls(
            day_of_month=day_of_month,
            day_of_week=day_of_week,
            hour=hour,
            minute=minute,
            month=month,
            year=year,
        )

        date_time_component.additional_properties = d
        return date_time_component

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
