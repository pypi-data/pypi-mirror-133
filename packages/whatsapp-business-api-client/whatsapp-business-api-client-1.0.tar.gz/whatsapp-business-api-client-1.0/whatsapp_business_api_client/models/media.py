from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.media_auto_download_item import MediaAutoDownloadItem

T = TypeVar("T", bound="Media")


@attr.s(auto_attribs=True)
class Media:
    """
    Example:
        {'auto_download': ['image', 'document', 'audio']}

    Attributes:
        auto_download (List[MediaAutoDownloadItem]): An array specifying which types of media to automatically download.
    """

    auto_download: List[MediaAutoDownloadItem]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        auto_download = []
        for auto_download_item_data in self.auto_download:
            auto_download_item = auto_download_item_data.value

            auto_download.append(auto_download_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "auto_download": auto_download,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        auto_download = []
        _auto_download = d.pop("auto_download")
        for auto_download_item_data in _auto_download:
            auto_download_item = MediaAutoDownloadItem(auto_download_item_data)

            auto_download.append(auto_download_item)

        media = cls(
            auto_download=auto_download,
        )

        media.additional_properties = d
        return media

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
