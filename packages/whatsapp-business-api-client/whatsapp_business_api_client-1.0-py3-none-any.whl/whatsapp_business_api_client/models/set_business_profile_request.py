from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="SetBusinessProfileRequest")


@attr.s(auto_attribs=True)
class SetBusinessProfileRequest:
    """
    Example:
        {'address': '<Business Profile Address>', 'description': '<Business Profile Description>', 'email': '<Business
            Profile Email>', 'vertical': '<Business Profile Vertical>', 'websites': ['https://www.whatsapp.com',
            'https://www.facebook.com']}

    Attributes:
        address (str): Address of the business
            Maximum of 256 characters
        description (str): Description of the business
            Maximum of 256 characters
        email (str): Email address to contact the business
            Maximum of 128 characters
        vertical (str): Industry of the business
            Maximum of 128 characters
        websites (List[str]): URLs associated with business (e.g., website, Facebook page, Instagram)
            Maximum of 2 websites with a maximum of 256 characters each
    """

    address: str
    description: str
    email: str
    vertical: str
    websites: List[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        address = self.address
        description = self.description
        email = self.email
        vertical = self.vertical
        websites = self.websites

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address": address,
                "description": description,
                "email": email,
                "vertical": vertical,
                "websites": websites,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address = d.pop("address")

        description = d.pop("description")

        email = d.pop("email")

        vertical = d.pop("vertical")

        websites = cast(List[str], d.pop("websites"))

        set_business_profile_request = cls(
            address=address,
            description=description,
            email=email,
            vertical=vertical,
            websites=websites,
        )

        set_business_profile_request.additional_properties = d
        return set_business_profile_request

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
