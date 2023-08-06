from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.provider import Provider

T = TypeVar("T", bound="ByProvider")


@attr.s(auto_attribs=True)
class ByProvider:
    """
    Example:
        {'caption': '<Message Caption>', 'link': '<Link to Video, https>', 'provider': {'name': '<Provider Name from
            Media Provider API, optional'}}

    Attributes:
        caption (str):
        link (str):
        provider (Provider):  Example: {'name': '<Provider Name from Media Provider API, optional'}.
    """

    caption: str
    link: str
    provider: Provider
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        caption = self.caption
        link = self.link
        provider = self.provider.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "caption": caption,
                "link": link,
                "provider": provider,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        caption = d.pop("caption")

        link = d.pop("link")

        provider = Provider.from_dict(d.pop("provider"))

        by_provider = cls(
            caption=caption,
            link=link,
            provider=provider,
        )

        by_provider.additional_properties = d
        return by_provider

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
