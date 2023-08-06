from enum import Enum


class CheckContactStatus(str, Enum):
    PROCESSING = "processing"
    VALID = "valid"
    INVALID = "invalid"

    def __str__(self) -> str:
        return str(self.value)
