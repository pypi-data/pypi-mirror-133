from enum import Enum


class SendTextMessageRequestRecipientType(str, Enum):
    INDIVIDUAL = "individual"
    GROUP = "group"

    def __str__(self) -> str:
        return str(self.value)
