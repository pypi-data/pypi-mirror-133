from enum import Enum


class MediaAutoDownloadItem(str, Enum):
    AUDIO = "audio"
    DOCUMENT = "document"
    VOICE = "voice"
    VIDEO = "video"
    IMAGE = "image."

    def __str__(self) -> str:
        return str(self.value)
