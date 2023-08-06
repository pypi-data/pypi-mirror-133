from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.contact import Contact
from ..models.error import Error
from ..models.message_type import MessageType
from ..models.root_type_for_message_context import RootTypeForMessageContext
from ..models.root_type_for_webhook_audio import RootTypeForWebhookAudio
from ..models.root_type_for_webhook_document import RootTypeForWebhookDocument
from ..models.root_type_for_webhook_image import RootTypeForWebhookImage
from ..models.root_type_for_webhook_location import RootTypeForWebhookLocation
from ..models.root_type_for_webhook_system import RootTypeForWebhookSystem
from ..models.root_type_for_webhook_text import RootTypeForWebhookText
from ..models.root_type_for_webhook_video import RootTypeForWebhookVideo
from ..models.root_type_for_webhook_voice import RootTypeForWebhookVoice
from ..types import UNSET, Unset

T = TypeVar("T", bound="RootTypeForWebhookMessage")


@attr.s(auto_attribs=True)
class RootTypeForWebhookMessage:
    """
    Example:
        {'from': '16315551234', 'id': 'ABGGFlA5FpafAgo6tHcNmNjXmuSf', 'text': {'body': 'Hello this is an answer'},
            'timestamp': '1518694235', 'type': 'text'}

    Attributes:
        audio (Union[Unset, RootTypeForWebhookAudio]):  Example: {'file': 'absolute-filepath-on-coreapp', 'id': 'media-
            id', 'link': 'link-to-audio-file', 'mime_type': 'media-mime-type', 'sha256': 'checksum'}.
        contacts (Union[Unset, List[Contact]]):
        context (Union[Unset, RootTypeForMessageContext]):  Example: {'from': 'sender-wa-id-of-context-message',
            'group_id': 'group-id-of-context-message', 'id': 'message-id-of-context-message', 'mentions': ['wa-id1', 'wa-
            id2']}.
        document (Union[Unset, RootTypeForWebhookDocument]):  Example: {'caption': '80skaraokesonglistartist', 'file':
            '/usr/local/wamedia/shared/fc233119-733f-49c-bcbd-b2f68f798e33', 'id': 'fc233119-733f-49c-bcbd-b2f68f798e33',
            'mime_type': 'application/pdf', 'sha256': '3b11fa6ef2bde1dd14726e09d3edaf782120919d06f6484f32d5d5caa4b8e'}.
        errors (Union[Unset, List[Error]]):
        from_ (Union[Unset, str]): WhatsApp ID of the sender
        group_id (Union[Unset, str]): Optional. WhatsApp group ID
        id (Union[Unset, str]): Message ID
        image (Union[Unset, RootTypeForWebhookImage]):  Example: {'caption': 'Check out my new phone!', 'file':
            '/usr/local/wamedia/shared/b1cf38-8734-4ad3-b4a1-ef0c10d0d683', 'id': 'b1c68f38-8734-4ad3-b4a1-ef0c10d683',
            'mime_type': 'image/jpeg', 'sha256': '29ed500fa64eb55fc19dc4124acb300e5dcc54a0f822a301ae99944db'}.
        location (Union[Unset, RootTypeForWebhookLocation]):  Example: {'address': 'Main Street Beach, Santa Cruz, CA',
            'latitude': 38.9806263495, 'longitude': -131.9428612257, 'name': 'Main Street Beach', 'url':
            'https://foursquare.com/v/4d7031d35b5df7744'}.
        system (Union[Unset, RootTypeForWebhookSystem]):  Example: {'body': '+1 (650) 387-5246 added +1 (650) 644-8470',
            'group_id': '16315558032-1530825318', 'operator': '16503875246', 'type': 'group_user_joined', 'users':
            ['16506448470']}.
        text (Union[Unset, RootTypeForWebhookText]):  Example: {'body': 'text-message-content'}.
        timestamp (Union[Unset, str]): Message received timestamp
        type (Union[Unset, MessageType]): type of the message Default: MessageType.TEXT.
        video (Union[Unset, RootTypeForWebhookVideo]):  Example: {'file': 'absolute-filepath-on-coreapp', 'id': 'media-
            id', 'link': 'link-to-video-file', 'mime_type': 'media-mime-type', 'sha256': 'checksum'}.
        voice (Union[Unset, RootTypeForWebhookVoice]):  Example: {'file':
            '/usr/local/wamedia/shared/463e/b7ec/ff4e4d9bb1101879cbd411b2', 'id': '463eb7ec-ff4e-4d9b-b110-1879cbd411b2',
            'mime_type': 'audio/ogg; codecs=opus', 'sha256':
            'fa9e1807d936b7cebe63654ea3a7912b1fa9479220258d823590521ef53b0710'}.
    """

    audio: Union[Unset, RootTypeForWebhookAudio] = UNSET
    contacts: Union[Unset, List[Contact]] = UNSET
    context: Union[Unset, RootTypeForMessageContext] = UNSET
    document: Union[Unset, RootTypeForWebhookDocument] = UNSET
    errors: Union[Unset, List[Error]] = UNSET
    from_: Union[Unset, str] = UNSET
    group_id: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    image: Union[Unset, RootTypeForWebhookImage] = UNSET
    location: Union[Unset, RootTypeForWebhookLocation] = UNSET
    system: Union[Unset, RootTypeForWebhookSystem] = UNSET
    text: Union[Unset, RootTypeForWebhookText] = UNSET
    timestamp: Union[Unset, str] = UNSET
    type: Union[Unset, MessageType] = MessageType.TEXT
    video: Union[Unset, RootTypeForWebhookVideo] = UNSET
    voice: Union[Unset, RootTypeForWebhookVoice] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        audio: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.audio, Unset):
            audio = self.audio.to_dict()

        contacts: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.contacts, Unset):
            contacts = []
            for contacts_item_data in self.contacts:
                contacts_item = contacts_item_data.to_dict()

                contacts.append(contacts_item)

        context: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        document: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.document, Unset):
            document = self.document.to_dict()

        errors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for errors_item_data in self.errors:
                errors_item = errors_item_data.to_dict()

                errors.append(errors_item)

        from_ = self.from_
        group_id = self.group_id
        id = self.id
        image: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_dict()

        location: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.location, Unset):
            location = self.location.to_dict()

        system: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.system, Unset):
            system = self.system.to_dict()

        text: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.text, Unset):
            text = self.text.to_dict()

        timestamp = self.timestamp
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        video: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.video, Unset):
            video = self.video.to_dict()

        voice: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.voice, Unset):
            voice = self.voice.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if audio is not UNSET:
            field_dict["audio"] = audio
        if contacts is not UNSET:
            field_dict["contacts"] = contacts
        if context is not UNSET:
            field_dict["context"] = context
        if document is not UNSET:
            field_dict["document"] = document
        if errors is not UNSET:
            field_dict["errors"] = errors
        if from_ is not UNSET:
            field_dict["from"] = from_
        if group_id is not UNSET:
            field_dict["group_id"] = group_id
        if id is not UNSET:
            field_dict["id"] = id
        if image is not UNSET:
            field_dict["image"] = image
        if location is not UNSET:
            field_dict["location"] = location
        if system is not UNSET:
            field_dict["system"] = system
        if text is not UNSET:
            field_dict["text"] = text
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if type is not UNSET:
            field_dict["type"] = type
        if video is not UNSET:
            field_dict["video"] = video
        if voice is not UNSET:
            field_dict["voice"] = voice

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _audio = d.pop("audio", UNSET)
        audio: Union[Unset, RootTypeForWebhookAudio]
        if isinstance(_audio, Unset):
            audio = UNSET
        else:
            audio = RootTypeForWebhookAudio.from_dict(_audio)

        contacts = []
        _contacts = d.pop("contacts", UNSET)
        for contacts_item_data in _contacts or []:
            contacts_item = Contact.from_dict(contacts_item_data)

            contacts.append(contacts_item)

        _context = d.pop("context", UNSET)
        context: Union[Unset, RootTypeForMessageContext]
        if isinstance(_context, Unset):
            context = UNSET
        else:
            context = RootTypeForMessageContext.from_dict(_context)

        _document = d.pop("document", UNSET)
        document: Union[Unset, RootTypeForWebhookDocument]
        if isinstance(_document, Unset):
            document = UNSET
        else:
            document = RootTypeForWebhookDocument.from_dict(_document)

        errors = []
        _errors = d.pop("errors", UNSET)
        for errors_item_data in _errors or []:
            errors_item = Error.from_dict(errors_item_data)

            errors.append(errors_item)

        from_ = d.pop("from", UNSET)

        group_id = d.pop("group_id", UNSET)

        id = d.pop("id", UNSET)

        _image = d.pop("image", UNSET)
        image: Union[Unset, RootTypeForWebhookImage]
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = RootTypeForWebhookImage.from_dict(_image)

        _location = d.pop("location", UNSET)
        location: Union[Unset, RootTypeForWebhookLocation]
        if isinstance(_location, Unset):
            location = UNSET
        else:
            location = RootTypeForWebhookLocation.from_dict(_location)

        _system = d.pop("system", UNSET)
        system: Union[Unset, RootTypeForWebhookSystem]
        if isinstance(_system, Unset):
            system = UNSET
        else:
            system = RootTypeForWebhookSystem.from_dict(_system)

        _text = d.pop("text", UNSET)
        text: Union[Unset, RootTypeForWebhookText]
        if isinstance(_text, Unset):
            text = UNSET
        else:
            text = RootTypeForWebhookText.from_dict(_text)

        timestamp = d.pop("timestamp", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, MessageType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = MessageType(_type)

        _video = d.pop("video", UNSET)
        video: Union[Unset, RootTypeForWebhookVideo]
        if isinstance(_video, Unset):
            video = UNSET
        else:
            video = RootTypeForWebhookVideo.from_dict(_video)

        _voice = d.pop("voice", UNSET)
        voice: Union[Unset, RootTypeForWebhookVoice]
        if isinstance(_voice, Unset):
            voice = UNSET
        else:
            voice = RootTypeForWebhookVoice.from_dict(_voice)

        root_type_for_webhook_message = cls(
            audio=audio,
            contacts=contacts,
            context=context,
            document=document,
            errors=errors,
            from_=from_,
            group_id=group_id,
            id=id,
            image=image,
            location=location,
            system=system,
            text=text,
            timestamp=timestamp,
            type=type,
            video=video,
            voice=voice,
        )

        root_type_for_webhook_message.additional_properties = d
        return root_type_for_webhook_message

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
