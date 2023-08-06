from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.root_type_for_webhook_contact_profile import RootTypeForWebhookContactProfile
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForWebhookContact")


@attr.s(auto_attribs=True)
class RootTypeForWebhookContact:
    """
    Example:
        {'profile': {'name': 'Kerry Fisher'}, 'wa_id': '16315551234'}

    Attributes:
        profile (Union[Unset, RootTypeForWebhookContactProfile]):  Example: {'name': 'sender-profile-name'}.
        wa_id (Union[Unset, str]): The WhatsApp ID of the contact
    """

    profile: Union[Unset, RootTypeForWebhookContactProfile] = UNSET
    wa_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        profile: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.profile, Unset):
            profile = self.profile.to_dict()

        wa_id = self.wa_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if profile is not UNSET:
            field_dict["profile"] = profile
        if wa_id is not UNSET:
            field_dict["wa_id"] = wa_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _profile = d.pop("profile", UNSET)
        profile: Union[Unset, RootTypeForWebhookContactProfile]
        if isinstance(_profile, Unset):
            profile = UNSET
        else:
            profile = RootTypeForWebhookContactProfile.from_dict(_profile)

        wa_id = d.pop("wa_id", UNSET)

        root_type_for_webhook_contact = cls(
            profile=profile,
            wa_id=wa_id,
        )

        root_type_for_webhook_contact.additional_properties = d
        return root_type_for_webhook_contact

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
