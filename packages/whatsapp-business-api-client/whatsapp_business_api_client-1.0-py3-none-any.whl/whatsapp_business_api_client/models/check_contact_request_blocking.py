from enum import Enum


class CheckContactRequestBlocking(str, Enum):
    NO_WAIT = "no_wait"
    WAIT = "wait"

    def __str__(self) -> str:
        return str(self.value)
