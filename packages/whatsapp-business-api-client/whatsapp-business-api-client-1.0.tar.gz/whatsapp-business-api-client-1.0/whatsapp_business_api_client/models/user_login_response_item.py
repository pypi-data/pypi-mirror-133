import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserLoginResponseItem")


@attr.s(auto_attribs=True)
class UserLoginResponseItem:
    """
    Example:
        {'expires_after': datetime.datetime(2018, 3, 1, 15, 29, 26, tzinfo=datetime.timezone.utc), 'token':
            'eyJhbGciOHlXVCJ9.eyJ1c2VyIjoNTIzMDE2Nn0.mEoF0COaO00Z1cANo'}

    Attributes:
        expires_after (Union[Unset, datetime.datetime]): Token expiration timestamp. By default, this is 7 days.
        token (Union[Unset, str]): Authentication token to be used for all other WhatsApp Business API calls. The token
            must be sent in the authorization header in the format:
            Authorization: Bearer <authentication-token>
    """

    expires_after: Union[Unset, datetime.datetime] = UNSET
    token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        expires_after: Union[Unset, str] = UNSET
        if not isinstance(self.expires_after, Unset):
            expires_after = self.expires_after.isoformat()

        token = self.token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if expires_after is not UNSET:
            field_dict["expires_after"] = expires_after
        if token is not UNSET:
            field_dict["token"] = token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _expires_after = d.pop("expires_after", UNSET)
        expires_after: Union[Unset, datetime.datetime]
        if isinstance(_expires_after, Unset):
            expires_after = UNSET
        else:
            expires_after = isoparse(_expires_after)

        token = d.pop("token", UNSET)

        user_login_response_item = cls(
            expires_after=expires_after,
            token=token,
        )

        user_login_response_item.additional_properties = d
        return user_login_response_item

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
