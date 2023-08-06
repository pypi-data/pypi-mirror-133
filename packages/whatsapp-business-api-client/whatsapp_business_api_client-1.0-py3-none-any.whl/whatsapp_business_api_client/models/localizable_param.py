from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.currency import Currency
from ..models.date_time import DateTime
from ..types import UNSET, Unset

T = TypeVar("T", bound="LocalizableParam")


@attr.s(auto_attribs=True)
class LocalizableParam:
    """
    Example:
        {'default': '<param value>'}

    Attributes:
        default (str): Default text if localization fails
        currency (Union[Unset, Currency]):  Example: {'amount_1000': 100990, 'currency_code': 'USD'}.
        date_time (Union[Unset, DateTime]): The Whatsapp Business API Client will attempt to format the date/time based
            on a specified localization. Example: {'component': {'day_of_month': 25, 'day_of_week': 5, 'hour': 15, 'minute':
            33, 'month': 2, 'year': 1977}}.
    """

    default: str
    currency: Union[Unset, Currency] = UNSET
    date_time: Union[Unset, DateTime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        default = self.default
        currency: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.currency, Unset):
            currency = self.currency.to_dict()

        date_time: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.date_time, Unset):
            date_time = self.date_time.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "default": default,
            }
        )
        if currency is not UNSET:
            field_dict["currency"] = currency
        if date_time is not UNSET:
            field_dict["date_time"] = date_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        default = d.pop("default")

        _currency = d.pop("currency", UNSET)
        currency: Union[Unset, Currency]
        if isinstance(_currency, Unset):
            currency = UNSET
        else:
            currency = Currency.from_dict(_currency)

        _date_time = d.pop("date_time", UNSET)
        date_time: Union[Unset, DateTime]
        if isinstance(_date_time, Unset):
            date_time = UNSET
        else:
            date_time = DateTime.from_dict(_date_time)

        localizable_param = cls(
            default=default,
            currency=currency,
            date_time=date_time,
        )

        localizable_param.additional_properties = d
        return localizable_param

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
