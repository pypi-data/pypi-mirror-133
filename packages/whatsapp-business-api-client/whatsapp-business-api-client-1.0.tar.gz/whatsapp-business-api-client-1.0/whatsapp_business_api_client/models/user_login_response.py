from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.error import Error
from ..models.meta import Meta
from ..models.user_login_response_item import UserLoginResponseItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserLoginResponse")


@attr.s(auto_attribs=True)
class UserLoginResponse:
    """
    Example:
        {'users': [{'expires_after': datetime.datetime(2018, 3, 1, 15, 29, 26, tzinfo=datetime.timezone.utc), 'token':
            'eyJhbGciOHlXVCJ9.eyJ1c2VyIjoNTIzMDE2Nn0.mEoF0COaO00Z1cANo'}]}

    Attributes:
        errors (Union[Unset, List[Error]]): Only returned with a failed request. Contains an array of error objects that
            are present when there is an error.
        meta (Union[Unset, Meta]): Contains generic information such as WhatsApp Business API Client version. Example:
            {'api_status': 'stable', 'version': 'whatsapp-business-api-client-version'}.
        users (Union[Unset, List[UserLoginResponseItem]]):
    """

    errors: Union[Unset, List[Error]] = UNSET
    meta: Union[Unset, Meta] = UNSET
    users: Union[Unset, List[UserLoginResponseItem]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        errors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for errors_item_data in self.errors:
                errors_item = errors_item_data.to_dict()

                errors.append(errors_item)

        meta: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()

                users.append(users_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if errors is not UNSET:
            field_dict["errors"] = errors
        if meta is not UNSET:
            field_dict["meta"] = meta
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        errors = []
        _errors = d.pop("errors", UNSET)
        for errors_item_data in _errors or []:
            errors_item = Error.from_dict(errors_item_data)

            errors.append(errors_item)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, Meta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = Meta.from_dict(_meta)

        users = []
        _users = d.pop("users", UNSET)
        for users_item_data in _users or []:
            users_item = UserLoginResponseItem.from_dict(users_item_data)

            users.append(users_item)

        user_login_response = cls(
            errors=errors,
            meta=meta,
            users=users,
        )

        user_login_response.additional_properties = d
        return user_login_response

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
