from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForWebhookVideo")


@attr.s(auto_attribs=True)
class RootTypeForWebhookVideo:
    """
    Example:
        {'file': 'absolute-filepath-on-coreapp', 'id': 'media-id', 'link': 'link-to-video-file', 'mime_type': 'media-
            mime-type', 'sha256': 'checksum'}

    Attributes:
        caption (Union[Unset, str]): Optional. Only present if specified.
        file (Union[Unset, str]): Absolute filename and location on media volume. This parameter is deprecated.
        id (Union[Unset, str]): ID of the media. Can be used to delete the media if stored locally on the client.
        link (Union[Unset, str]):
        mime_type (Union[Unset, str]): Mime type of media
        sha256 (Union[Unset, str]): Checksum
    """

    caption: Union[Unset, str] = UNSET
    file: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    link: Union[Unset, str] = UNSET
    mime_type: Union[Unset, str] = UNSET
    sha256: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        caption = self.caption
        file = self.file
        id = self.id
        link = self.link
        mime_type = self.mime_type
        sha256 = self.sha256

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if caption is not UNSET:
            field_dict["caption"] = caption
        if file is not UNSET:
            field_dict["file"] = file
        if id is not UNSET:
            field_dict["id"] = id
        if link is not UNSET:
            field_dict["link"] = link
        if mime_type is not UNSET:
            field_dict["mime_type"] = mime_type
        if sha256 is not UNSET:
            field_dict["sha256"] = sha256

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        caption = d.pop("caption", UNSET)

        file = d.pop("file", UNSET)

        id = d.pop("id", UNSET)

        link = d.pop("link", UNSET)

        mime_type = d.pop("mime_type", UNSET)

        sha256 = d.pop("sha256", UNSET)

        root_type_for_webhook_video = cls(
            caption=caption,
            file=file,
            id=id,
            link=link,
            mime_type=mime_type,
            sha256=sha256,
        )

        root_type_for_webhook_video.additional_properties = d
        return root_type_for_webhook_video

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
