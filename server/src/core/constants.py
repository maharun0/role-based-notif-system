from enum import StrEnum


class RoleName(StrEnum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    EDITOR = "Editor"
    VIEWER = "Viewer"
    SUPPORT = "Support"


class AudienceType(StrEnum):
    ALL = "ALL"
    BY_ROLE = "BY_ROLE"
