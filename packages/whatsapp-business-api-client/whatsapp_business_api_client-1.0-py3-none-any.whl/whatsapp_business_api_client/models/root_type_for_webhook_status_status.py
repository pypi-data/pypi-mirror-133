from enum import Enum


class RootTypeForWebhookStatusStatus(str, Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    DELETED = "deleted"

    def __str__(self) -> str:
        return str(self.value)
