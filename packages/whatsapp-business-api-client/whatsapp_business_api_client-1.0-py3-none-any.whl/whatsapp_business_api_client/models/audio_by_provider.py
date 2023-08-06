from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.provider import Provider

T = TypeVar("T", bound="AudioByProvider")


@attr.s(auto_attribs=True)
class AudioByProvider:
    """
    Example:
        {'link': '<Link to Audio, https>', 'provider': {'name': '<Provider Name from Media Provider API, optional'}}

    Attributes:
        link (str):
        provider (Provider):  Example: {'name': '<Provider Name from Media Provider API, optional'}.
    """

    link: str
    provider: Provider
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        link = self.link
        provider = self.provider.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "link": link,
                "provider": provider,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        link = d.pop("link")

        provider = Provider.from_dict(d.pop("provider"))

        audio_by_provider = cls(
            link=link,
            provider=provider,
        )

        audio_by_provider.additional_properties = d
        return audio_by_provider

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
