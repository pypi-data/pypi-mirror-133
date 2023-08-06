from enum import Enum


class RootTypeForGatewayNodeStatusRole(str, Enum):
    PRIMARY_MASTER = "primary_master"
    SECONDARY_MASTER = "secondary_master"
    COREAPP = "coreapp"

    def __str__(self) -> str:
        return str(self.value)
