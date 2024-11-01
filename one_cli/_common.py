from dataclasses    import dataclass



@dataclass
class UnitPermissions:
    USE:    bool
    MANAGE: bool
    ADMIN:  bool


@dataclass
class Permissions:
    OWNER:  UnitPermissions
    GROUP:  UnitPermissions
    OTHER:  UnitPermissions



@dataclass
class LockStatus:
    LOCKED:     int
    OWNER:      int
    TIME:       int
    REQ_ID:     int

