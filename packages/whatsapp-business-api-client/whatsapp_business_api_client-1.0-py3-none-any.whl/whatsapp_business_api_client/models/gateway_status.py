from enum import Enum


class GatewayStatus(str, Enum):
    CONNECTED = "connected"
    CONNECTING = "connecting"
    DISCONNECTED = "disconnected"
    UNINITIALIZED = "uninitialized"
    UNREGISTERED = "unregistered"

    def __str__(self) -> str:
        return str(self.value)
