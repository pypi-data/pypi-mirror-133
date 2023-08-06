from enum import Enum


class LanguagePolicy(str, Enum):
    FALLBACK = "fallback"
    DETERMINISTIC = "deterministic"

    def __str__(self) -> str:
        return str(self.value)
