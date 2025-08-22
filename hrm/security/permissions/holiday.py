import enum
from care.security.permissions.constants import Permission, PermissionContext
from care.security.roles.role import (
    ADMIN_ROLE,
    FACILITY_ADMIN_ROLE,
    ADMINISTRATOR,
    STAFF_ROLE,
    DOCTOR_ROLE,
    NURSE_ROLE,
    VOLUNTEER_ROLE,
)

employee_roles = [
    STAFF_ROLE,
    DOCTOR_ROLE,
    NURSE_ROLE,
    VOLUNTEER_ROLE,
    ADMIN_ROLE,
    FACILITY_ADMIN_ROLE,
    ADMINISTRATOR,
]

hr_roles = [
    ADMIN_ROLE,
    FACILITY_ADMIN_ROLE,
    ADMINISTRATOR,
]

class HolidayPermissions(enum.Enum):
    can_list_holidays = Permission(
        "Can List Holidays",
        "",
        PermissionContext.FACILITY,
        employee_roles,
    )
    can_create_holiday = Permission(
        "Can Create Holiday",
        "",
        PermissionContext.FACILITY,
        hr_roles,
    )
    can_update_holiday = Permission(
        "Can Update Holiday",
        "",
        PermissionContext.FACILITY,
        hr_roles,
    )
    can_delete_holiday = Permission(
        "Can Delete Holiday",
        "",
        PermissionContext.FACILITY,
        hr_roles,
    )