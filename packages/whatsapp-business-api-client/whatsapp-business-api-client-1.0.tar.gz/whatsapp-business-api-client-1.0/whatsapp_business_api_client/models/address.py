from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="Address")


@attr.s(auto_attribs=True)
class Address:
    """
    Example:
        {'city': 'Menlo Park', 'country': 'United States', 'country_code': 'us', 'state': 'CA', 'street': '1 Hacker
            Way', 'type': 'HOME', 'zip': '94025'}

    Attributes:
        city (str): City name
        country (str): Full country name
        country_code (str): Two-letter country abbreviation
        state (str): State abbreviation
        street (str): Street number and name
        type (str): Standard Values: HOME, WORK
        zip_ (str): ZIP code
    """

    city: str
    country: str
    country_code: str
    state: str
    street: str
    type: str
    zip_: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        city = self.city
        country = self.country
        country_code = self.country_code
        state = self.state
        street = self.street
        type = self.type
        zip_ = self.zip_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "city": city,
                "country": country,
                "country_code": country_code,
                "state": state,
                "street": street,
                "type": type,
                "zip": zip_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        city = d.pop("city")

        country = d.pop("country")

        country_code = d.pop("country_code")

        state = d.pop("state")

        street = d.pop("street")

        type = d.pop("type")

        zip_ = d.pop("zip")

        address = cls(
            city=city,
            country=country,
            country_code=country_code,
            state=state,
            street=street,
            type=type,
            zip_=zip_,
        )

        address.additional_properties = d
        return address

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
