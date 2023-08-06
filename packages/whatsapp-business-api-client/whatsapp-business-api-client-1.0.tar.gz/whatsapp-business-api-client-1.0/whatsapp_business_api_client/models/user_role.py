from enum import Enum


class UserRole(str, Enum):
    ROLE_ADMIN = "ROLE_ADMIN"
    ROLE_USER = "ROLE_USER"

    def __str__(self) -> str:
        return str(self.value)
