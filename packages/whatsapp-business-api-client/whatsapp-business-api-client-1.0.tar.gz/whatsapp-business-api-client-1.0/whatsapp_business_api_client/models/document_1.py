from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.provider import Provider

T = TypeVar("T", bound="Document1")


@attr.s(auto_attribs=True)
class Document1:
    """
    Example:
        {'caption': '<Message Caption>', 'filename': '<Filename>', 'link': '<Link to PDF, https>', 'provider': {'name':
            '<Provider Name from Media Provider API, optional'}}

    Attributes:
        caption (str):
        filename (str):
        link (str):
        provider (Provider):  Example: {'name': '<Provider Name from Media Provider API, optional'}.
    """

    caption: str
    filename: str
    link: str
    provider: Provider
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        caption = self.caption
        filename = self.filename
        link = self.link
        provider = self.provider.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "caption": caption,
                "filename": filename,
                "link": link,
                "provider": provider,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        caption = d.pop("caption")

        filename = d.pop("filename")

        link = d.pop("link")

        provider = Provider.from_dict(d.pop("provider"))

        document_1 = cls(
            caption=caption,
            filename=filename,
            link=link,
            provider=provider,
        )

        document_1.additional_properties = d
        return document_1

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
