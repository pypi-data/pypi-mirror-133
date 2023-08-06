from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="Location")


@attr.s(auto_attribs=True)
class Location:
    """
    Example:
        {'address': "<Location's Address>", 'latitude': '<Latitude>', 'longitude': '<Longitude>', 'name': '<Location
            Name>'}

    Attributes:
        address (str): Address of the location. Only displayed if name is present.
        latitude (str): Latitude of the location
        longitude (str): Longitude of the location
        name (str): Name of the location
    """

    address: str
    latitude: str
    longitude: str
    name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        address = self.address
        latitude = self.latitude
        longitude = self.longitude
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address": address,
                "latitude": latitude,
                "longitude": longitude,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address = d.pop("address")

        latitude = d.pop("latitude")

        longitude = d.pop("longitude")

        name = d.pop("name")

        location = cls(
            address=address,
            latitude=latitude,
            longitude=longitude,
            name=name,
        )

        location.additional_properties = d
        return location

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
