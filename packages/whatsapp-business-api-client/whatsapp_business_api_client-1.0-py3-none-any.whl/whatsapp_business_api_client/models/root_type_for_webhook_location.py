from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForWebhookLocation")


@attr.s(auto_attribs=True)
class RootTypeForWebhookLocation:
    """
    Example:
        {'address': 'Main Street Beach, Santa Cruz, CA', 'latitude': 38.9806263495, 'longitude': -131.9428612257,
            'name': 'Main Street Beach', 'url': 'https://foursquare.com/v/4d7031d35b5df7744'}

    Attributes:
        address (Union[Unset, str]): Address of the location
        latitude (Union[Unset, float]): Latitude of location being sent
        longitude (Union[Unset, float]): Longitude of location being sent
        name (Union[Unset, str]): Name of the location
        url (Union[Unset, str]): URL for the website where the user downloaded the location information
    """

    address: Union[Unset, str] = UNSET
    latitude: Union[Unset, float] = UNSET
    longitude: Union[Unset, float] = UNSET
    name: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        address = self.address
        latitude = self.latitude
        longitude = self.longitude
        name = self.name
        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if address is not UNSET:
            field_dict["address"] = address
        if latitude is not UNSET:
            field_dict["latitude"] = latitude
        if longitude is not UNSET:
            field_dict["longitude"] = longitude
        if name is not UNSET:
            field_dict["name"] = name
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address = d.pop("address", UNSET)

        latitude = d.pop("latitude", UNSET)

        longitude = d.pop("longitude", UNSET)

        name = d.pop("name", UNSET)

        url = d.pop("url", UNSET)

        root_type_for_webhook_location = cls(
            address=address,
            latitude=latitude,
            longitude=longitude,
            name=name,
            url=url,
        )

        root_type_for_webhook_location.additional_properties = d
        return root_type_for_webhook_location

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
