from enum import Enum


class MetaApiStatus(str, Enum):
    DEPRECATED = "deprecated"
    EXPERIMENTAL = "experimental"
    STABLE = "stable"

    def __str__(self) -> str:
        return str(self.value)
