import enum
from care.security.permissions.constants import Permission, PermissionContext
from care.security.roles.role import (
    ADMIN_ROLE,
)

class EmployeePermissions(enum.Enum):
    can_list_employees = Permission(
        "Can List Employees",
        "",
        PermissionContext.FACILITY,
        [ADMIN_ROLE],
    )
    can_create_employee = Permission(
        "Can Create Employee",
        "",
        PermissionContext.FACILITY,
        [ADMIN_ROLE],
    )
    can_update_employee = Permission(
        "Can Update Employee",
        "",
        PermissionContext.FACILITY,
        [ADMIN_ROLE],
    )
    can_delete_employee = Permission(
        "Can Delete Employee",
        "",
        PermissionContext.FACILITY,
        [ADMIN_ROLE],
    )
    can_view_employee_details = Permission(
        "Can View Employee Details",
        "",
        PermissionContext.FACILITY,
        [ADMIN_ROLE],
    )
