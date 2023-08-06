from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.root_type_for_request_code_account import RootTypeForRequestCodeAccount
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForRequestCodeResponse")


@attr.s(auto_attribs=True)
class RootTypeForRequestCodeResponse:
    """
    Example:
        {'account': [{'vname': 'decoded-vname-from-cert'}]}

    Attributes:
        account (Union[Unset, List[RootTypeForRequestCodeAccount]]):
    """

    account: Union[Unset, List[RootTypeForRequestCodeAccount]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.account, Unset):
            account = []
            for account_item_data in self.account:
                account_item = account_item_data.to_dict()

                account.append(account_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account is not UNSET:
            field_dict["account"] = account

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        account = []
        _account = d.pop("account", UNSET)
        for account_item_data in _account or []:
            account_item = RootTypeForRequestCodeAccount.from_dict(account_item_data)

            account.append(account_item)

        root_type_for_request_code_response = cls(
            account=account,
        )

        root_type_for_request_code_response.additional_properties = d
        return root_type_for_request_code_response

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
