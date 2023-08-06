from enum import Enum


class MessageType(str, Enum):
    AUDIO = "audio"
    CONTACTS = "contacts"
    DOCUMENT = "document"
    HSM = "hsm"
    IMAGE = "image"
    LOCATION = "location"
    TEXT = "text"
    VIDEO = "video"
    VOICE = "voice"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
