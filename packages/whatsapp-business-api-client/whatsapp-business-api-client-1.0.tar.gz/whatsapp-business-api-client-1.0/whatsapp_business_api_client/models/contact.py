from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.address import Address
from ..models.email import Email
from ..models.name import Name
from ..models.org import Org
from ..models.phone import Phone
from ..models.root_type_for_url import RootTypeForUrl
from ..types import UNSET, Unset

T = TypeVar("T", bound="Contact")


@attr.s(auto_attribs=True)
class Contact:
    """
    Example:
        {'addresses': [{'city': 'Menlo Park', 'country': 'United States', 'country_code': 'us', 'state': 'CA', 'street':
            '1 Hacker Way', 'type': 'HOME', 'zip': '94025'}, {'city': 'Menlo Park', 'country': 'United States',
            'country_code': 'us', 'state': 'CA', 'street': '200 Jefferson Dr', 'type': 'WORK', 'zip': '94025'}], 'birthday':
            datetime.date(2012, 8, 18), 'emails': [{'email': 'test@fb.com', 'type': 'WORK'}, {'email': 'test@whatsapp.com',
            'type': 'WORK'}], 'name': {'first_name': 'John', 'formatted_name': 'John Smith', 'last_name': 'Smith'}, 'org':
            {'company': 'WhatsApp', 'department': 'Design', 'title': 'Manager'}, 'phones': [{'phone': '+1 (940) 555-1234',
            'type': 'HOME'}, {'phone': '+1 (650) 555-1234', 'type': 'WORK', 'wa_id': '16505551234'}], 'urls': [{'type':
            'WORK', 'url': 'https://www.facebook.com'}]}

    Attributes:
        addresses (Union[Unset, List[Address]]): Full contact address(es)
        birthday (Union[Unset, str]): YYYY-MM-DD formatted string
        emails (Union[Unset, List[Email]]): Contact email address(es)
        ims (Union[Unset, List[str]]):
        name (Union[Unset, Name]): Full contact name Example: {'first_name': 'John', 'formatted_name': 'John Smith',
            'last_name': 'Smith'}.
        org (Union[Unset, Org]): Contact organization information Example: {'company': 'WhatsApp', 'department':
            'Design', 'title': 'Manager'}.
        phones (Union[Unset, List[Phone]]): Contact phone number(s)
        urls (Union[Unset, List[RootTypeForUrl]]): Contact URL(s)
    """

    addresses: Union[Unset, List[Address]] = UNSET
    birthday: Union[Unset, str] = UNSET
    emails: Union[Unset, List[Email]] = UNSET
    ims: Union[Unset, List[str]] = UNSET
    name: Union[Unset, Name] = UNSET
    org: Union[Unset, Org] = UNSET
    phones: Union[Unset, List[Phone]] = UNSET
    urls: Union[Unset, List[RootTypeForUrl]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        addresses: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.addresses, Unset):
            addresses = []
            for addresses_item_data in self.addresses:
                addresses_item = addresses_item_data.to_dict()

                addresses.append(addresses_item)

        birthday = self.birthday
        emails: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.emails, Unset):
            emails = []
            for emails_item_data in self.emails:
                emails_item = emails_item_data.to_dict()

                emails.append(emails_item)

        ims: Union[Unset, List[str]] = UNSET
        if not isinstance(self.ims, Unset):
            ims = self.ims

        name: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.to_dict()

        org: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.org, Unset):
            org = self.org.to_dict()

        phones: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.phones, Unset):
            phones = []
            for phones_item_data in self.phones:
                phones_item = phones_item_data.to_dict()

                phones.append(phones_item)

        urls: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.urls, Unset):
            urls = []
            for urls_item_data in self.urls:
                urls_item = urls_item_data.to_dict()

                urls.append(urls_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if addresses is not UNSET:
            field_dict["addresses"] = addresses
        if birthday is not UNSET:
            field_dict["birthday"] = birthday
        if emails is not UNSET:
            field_dict["emails"] = emails
        if ims is not UNSET:
            field_dict["ims"] = ims
        if name is not UNSET:
            field_dict["name"] = name
        if org is not UNSET:
            field_dict["org"] = org
        if phones is not UNSET:
            field_dict["phones"] = phones
        if urls is not UNSET:
            field_dict["urls"] = urls

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        addresses = []
        _addresses = d.pop("addresses", UNSET)
        for addresses_item_data in _addresses or []:
            addresses_item = Address.from_dict(addresses_item_data)

            addresses.append(addresses_item)

        birthday = d.pop("birthday", UNSET)

        emails = []
        _emails = d.pop("emails", UNSET)
        for emails_item_data in _emails or []:
            emails_item = Email.from_dict(emails_item_data)

            emails.append(emails_item)

        ims = cast(List[str], d.pop("ims", UNSET))

        _name = d.pop("name", UNSET)
        name: Union[Unset, Name]
        if isinstance(_name, Unset):
            name = UNSET
        else:
            name = Name.from_dict(_name)

        _org = d.pop("org", UNSET)
        org: Union[Unset, Org]
        if isinstance(_org, Unset):
            org = UNSET
        else:
            org = Org.from_dict(_org)

        phones = []
        _phones = d.pop("phones", UNSET)
        for phones_item_data in _phones or []:
            phones_item = Phone.from_dict(phones_item_data)

            phones.append(phones_item)

        urls = []
        _urls = d.pop("urls", UNSET)
        for urls_item_data in _urls or []:
            urls_item = RootTypeForUrl.from_dict(urls_item_data)

            urls.append(urls_item)

        contact = cls(
            addresses=addresses,
            birthday=birthday,
            emails=emails,
            ims=ims,
            name=name,
            org=org,
            phones=phones,
            urls=urls,
        )

        contact.additional_properties = d
        return contact

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
