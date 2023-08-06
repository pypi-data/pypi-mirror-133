from enum import Enum


class RequestCodeRequestMethod(str, Enum):
    SMS = "sms"
    VOICE = "voice"

    def __str__(self) -> str:
        return str(self.value)
