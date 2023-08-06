from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="VideoById")


@attr.s(auto_attribs=True)
class VideoById:
    """
    Example:
        {'caption': '<Message Caption>', 'id': '<Media Id, from Media API>'}

    Attributes:
        caption (str):
        id (str):
    """

    caption: str
    id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        caption = self.caption
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "caption": caption,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        caption = d.pop("caption")

        id = d.pop("id")

        video_by_id = cls(
            caption=caption,
            id=id,
        )

        video_by_id.additional_properties = d
        return video_by_id

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
