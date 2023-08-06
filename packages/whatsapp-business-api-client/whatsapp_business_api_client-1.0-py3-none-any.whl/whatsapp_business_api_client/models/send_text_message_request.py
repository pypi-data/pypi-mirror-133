from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.audio_by_id import AudioById
from ..models.audio_by_provider import AudioByProvider
from ..models.by_provider import ByProvider
from ..models.contact import Contact
from ..models.document import Document
from ..models.document_1 import Document1
from ..models.hsm import Hsm
from ..models.image_by_id import ImageById
from ..models.image_by_provider import ImageByProvider
from ..models.location import Location
from ..models.message_type import MessageType
from ..models.send_text_message_request_recipient_type import SendTextMessageRequestRecipientType
from ..models.send_text_message_request_ttl import SendTextMessageRequestTtl
from ..models.text import Text
from ..models.video_by_id import VideoById
from ..types import UNSET, Unset

T = TypeVar("T", bound="SendTextMessageRequest")


@attr.s(auto_attribs=True)
class SendTextMessageRequest:
    """
    Example:
        {'preview_url': True, 'recipient_type': 'individual', 'text': {'body': 'your-text-message-content'}, 'to':
            '{whatsapp-id}', 'type': 'text'}

    Attributes:
        to (str): When recipient_type is individual, this field is the WhatsApp ID (phone number) returned from contacts
            endpoint. When recipient_type is group, this field is the WhatsApp group ID.
        audio (Union[AudioById, AudioByProvider, Unset]): The media object containing audio
        contacts (Union[Unset, List[Contact]]):
        document (Union[Document, Document1, Unset]): The media object containing a document
        hsm (Union[Unset, Hsm]): The containing element for the message content — Indicates that the message is highly
            structured. Parameters contained within provide the structure. Example: {'element_name': 'hello_world',
            'language': {'code': 'en', 'policy': 'deterministic'}, 'localizable_params': [{'default': '1234'}], 'namespace':
            'business_a_namespace'}.
        image (Union[ImageById, ImageByProvider, Unset]): The media object containing an image
        location (Union[Unset, Location]):  Example: {'address': "<Location's Address>", 'latitude': '<Latitude>',
            'longitude': '<Longitude>', 'name': '<Location Name>'}.
        preview_url (Union[Unset, bool]): Specifying preview_url in the request is optional when not including a URL in
            your message.
            To include a URL preview, set preview_url to true in the message body and make sure the URL begins with http://
            or https://. For more information, see the Sending URLs in Text Messages section.
        recipient_type (Union[Unset, SendTextMessageRequestRecipientType]): Determines whether the recipient is an
            individual or a group
            Specifying recipient_type in the request is optional when the value is individual.
            However, recipient_type is required when using group. If sending a text message to a group, see the Sending
            Group Messages documentation. Default: SendTextMessageRequestRecipientType.INDIVIDUAL.
        text (Union[Unset, Text]):  Example: {'body': '<Message Text>'}.
        ttl (Union[Unset, SendTextMessageRequestTtl]):
        type (Union[Unset, MessageType]): type of the message Default: MessageType.TEXT.
        video (Union[ByProvider, Unset, VideoById]): The media object containing a video
    """

    to: str
    audio: Union[AudioById, AudioByProvider, Unset] = UNSET
    contacts: Union[Unset, List[Contact]] = UNSET
    document: Union[Document, Document1, Unset] = UNSET
    hsm: Union[Unset, Hsm] = UNSET
    image: Union[ImageById, ImageByProvider, Unset] = UNSET
    location: Union[Unset, Location] = UNSET
    preview_url: Union[Unset, bool] = UNSET
    recipient_type: Union[Unset, SendTextMessageRequestRecipientType] = SendTextMessageRequestRecipientType.INDIVIDUAL
    text: Union[Unset, Text] = UNSET
    ttl: Union[Unset, SendTextMessageRequestTtl] = UNSET
    type: Union[Unset, MessageType] = MessageType.TEXT
    video: Union[ByProvider, Unset, VideoById] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        to = self.to
        audio: Union[Dict[str, Any], Unset]
        if isinstance(self.audio, Unset):
            audio = UNSET
        elif isinstance(self.audio, AudioById):
            audio = self.audio.to_dict()

        else:
            audio = self.audio.to_dict()

        contacts: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.contacts, Unset):
            contacts = []
            for contacts_item_data in self.contacts:
                contacts_item = contacts_item_data.to_dict()

                contacts.append(contacts_item)

        document: Union[Dict[str, Any], Unset]
        if isinstance(self.document, Unset):
            document = UNSET
        elif isinstance(self.document, Document):
            document = self.document.to_dict()

        else:
            document = self.document.to_dict()

        hsm: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.hsm, Unset):
            hsm = self.hsm.to_dict()

        image: Union[Dict[str, Any], Unset]
        if isinstance(self.image, Unset):
            image = UNSET
        elif isinstance(self.image, ImageById):
            image = self.image.to_dict()

        else:
            image = self.image.to_dict()

        location: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.location, Unset):
            location = self.location.to_dict()

        preview_url = self.preview_url
        recipient_type: Union[Unset, str] = UNSET
        if not isinstance(self.recipient_type, Unset):
            recipient_type = self.recipient_type.value

        text: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.text, Unset):
            text = self.text.to_dict()

        ttl: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.ttl, Unset):
            ttl = self.ttl.to_dict()

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        video: Union[Dict[str, Any], Unset]
        if isinstance(self.video, Unset):
            video = UNSET
        elif isinstance(self.video, VideoById):
            video = self.video.to_dict()

        else:
            video = self.video.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "to": to,
            }
        )
        if audio is not UNSET:
            field_dict["audio"] = audio
        if contacts is not UNSET:
            field_dict["contacts"] = contacts
        if document is not UNSET:
            field_dict["document"] = document
        if hsm is not UNSET:
            field_dict["hsm"] = hsm
        if image is not UNSET:
            field_dict["image"] = image
        if location is not UNSET:
            field_dict["location"] = location
        if preview_url is not UNSET:
            field_dict["preview_url"] = preview_url
        if recipient_type is not UNSET:
            field_dict["recipient_type"] = recipient_type
        if text is not UNSET:
            field_dict["text"] = text
        if ttl is not UNSET:
            field_dict["ttl"] = ttl
        if type is not UNSET:
            field_dict["type"] = type
        if video is not UNSET:
            field_dict["video"] = video

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        to = d.pop("to")

        def _parse_audio(data: object) -> Union[AudioById, AudioByProvider, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_audio_type_0 = AudioById.from_dict(data)

                return componentsschemas_audio_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_audio_type_1 = AudioByProvider.from_dict(data)

            return componentsschemas_audio_type_1

        audio = _parse_audio(d.pop("audio", UNSET))

        contacts = []
        _contacts = d.pop("contacts", UNSET)
        for contacts_item_data in _contacts or []:
            contacts_item = Contact.from_dict(contacts_item_data)

            contacts.append(contacts_item)

        def _parse_document(data: object) -> Union[Document, Document1, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_document_type_0 = Document.from_dict(data)

                return componentsschemas_document_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_document_type_1 = Document1.from_dict(data)

            return componentsschemas_document_type_1

        document = _parse_document(d.pop("document", UNSET))

        _hsm = d.pop("hsm", UNSET)
        hsm: Union[Unset, Hsm]
        if isinstance(_hsm, Unset):
            hsm = UNSET
        else:
            hsm = Hsm.from_dict(_hsm)

        def _parse_image(data: object) -> Union[ImageById, ImageByProvider, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_image_type_0 = ImageById.from_dict(data)

                return componentsschemas_image_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_image_type_1 = ImageByProvider.from_dict(data)

            return componentsschemas_image_type_1

        image = _parse_image(d.pop("image", UNSET))

        _location = d.pop("location", UNSET)
        location: Union[Unset, Location]
        if isinstance(_location, Unset):
            location = UNSET
        else:
            location = Location.from_dict(_location)

        preview_url = d.pop("preview_url", UNSET)

        _recipient_type = d.pop("recipient_type", UNSET)
        recipient_type: Union[Unset, SendTextMessageRequestRecipientType]
        if isinstance(_recipient_type, Unset):
            recipient_type = UNSET
        else:
            recipient_type = SendTextMessageRequestRecipientType(_recipient_type)

        _text = d.pop("text", UNSET)
        text: Union[Unset, Text]
        if isinstance(_text, Unset):
            text = UNSET
        else:
            text = Text.from_dict(_text)

        _ttl = d.pop("ttl", UNSET)
        ttl: Union[Unset, SendTextMessageRequestTtl]
        if isinstance(_ttl, Unset):
            ttl = UNSET
        else:
            ttl = SendTextMessageRequestTtl.from_dict(_ttl)

        _type = d.pop("type", UNSET)
        type: Union[Unset, MessageType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = MessageType(_type)

        def _parse_video(data: object) -> Union[ByProvider, Unset, VideoById]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_video_type_0 = VideoById.from_dict(data)

                return componentsschemas_video_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_video_type_1 = ByProvider.from_dict(data)

            return componentsschemas_video_type_1

        video = _parse_video(d.pop("video", UNSET))

        send_text_message_request = cls(
            to=to,
            audio=audio,
            contacts=contacts,
            document=document,
            hsm=hsm,
            image=image,
            location=location,
            preview_url=preview_url,
            recipient_type=recipient_type,
            text=text,
            ttl=ttl,
            type=type,
            video=video,
        )

        send_text_message_request.additional_properties = d
        return send_text_message_request

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
