from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.request_code_request_method import RequestCodeRequestMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestCodeRequest")


@attr.s(auto_attribs=True)
class RequestCodeRequest:
    """
    Example:
        {'cc': '<Country Code>', 'cert': '<Valid Cert from Business Manager>', 'method': '< sms | voice >',
            'phone_number': '<Phone Number>', 'pin': '<Two-Step Verification PIN'}

    Attributes:
        cc (str): Numerical country code for the phone number you are registering
        cert (str): Base64-encoded Verified Name certificate
        method (RequestCodeRequestMethod): Method of receiving your registration code
        phone_number (str): Phone number you are registering, without the country code or plus symbol (+)
        pin (Union[Unset, str]): Existing 6-digit PIN — This is only required when two-factor verification is enabled on
            this account.
    """

    cc: str
    cert: str
    method: RequestCodeRequestMethod
    phone_number: str
    pin: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cc = self.cc
        cert = self.cert
        method = self.method.value

        phone_number = self.phone_number
        pin = self.pin

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cc": cc,
                "cert": cert,
                "method": method,
                "phone_number": phone_number,
            }
        )
        if pin is not UNSET:
            field_dict["pin"] = pin

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cc = d.pop("cc")

        cert = d.pop("cert")

        method = RequestCodeRequestMethod(d.pop("method"))

        phone_number = d.pop("phone_number")

        pin = d.pop("pin", UNSET)

        request_code_request = cls(
            cc=cc,
            cert=cert,
            method=method,
            phone_number=phone_number,
            pin=pin,
        )

        request_code_request.additional_properties = d
        return request_code_request

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
