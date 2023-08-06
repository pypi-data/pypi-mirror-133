from enum import Enum


class RootTypeForWebhookSystemType(str, Enum):
    GROUP_CREATED = "group_created"
    GROUP_USER_PROMOTED = "group_user_promoted"
    GROUP_USER_DEMOTED = "group_user_demoted"
    GROUP_USER_JOINED = "group_user_joined"
    GROUP_USER_LEFT = "group_user_left"
    GROUP_SUBJECT_CHANGED = "group_subject_changed"
    GROUP_DESCRIPTION_CHANGED = "group_description_changed"
    GROUP_ICON_CHANGED = "group_icon_changed"
    GROUP_ICON_DELETED = "group_icon_deleted"
    GROUP_INVITE_LINK_REVOKED = "group_invite_link_revoked"
    USER_IDENTITY_CHANGED = "user_identity_changed"
    GROUP_USER_CHANGED_NUMBER = "group_user_changed_number"
    GROUP_ERROR_FETCHING_PHOTO = "group_error_fetching_photo"
    GROUP_ERROR_ADDING_USERS = "group_error_adding_users"
    GROUP_ERROR_ADDING_USER = "group_error_adding_user"
    GROUP_ERROR_FULL_ADDING_USERS = "group_error_full_adding_users"
    GROUP_ERROR_REMOVING_USER = "group_error_removing_user"
    BROADCAST_LIST_CREATED = "broadcast_list_created"
    GROUP_ENDED = "group_ended"
    GROUP_ERROR_BLOCKED_ADDING_USER = "group_error_blocked_adding_user"

    def __str__(self) -> str:
        return str(self.value)
