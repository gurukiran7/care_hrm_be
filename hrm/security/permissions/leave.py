import enum
from care.security.permissions.constants import Permission, PermissionContext
from care.security.roles.role import (
    DOCTOR_ROLE,
    STAFF_ROLE,
    NURSE_ROLE,
    ADMINISTRATOR,
    FACILITY_ADMIN_ROLE,
    ADMIN_ROLE,
    VOLUNTEER_ROLE,
)

employee_roles = [
    DOCTOR_ROLE,
    STAFF_ROLE,
    NURSE_ROLE,
    ADMIN_ROLE,
    FACILITY_ADMIN_ROLE,
    ADMINISTRATOR,
]

hr_roles = [
    ADMIN_ROLE,
    FACILITY_ADMIN_ROLE,
    ADMINISTRATOR,
]

class LeavePermissions(enum.Enum):
    can_list_leave_requests = Permission(
        "Can List Leave Requests",
        "",
        PermissionContext.FACILITY,
        employee_roles,
    )
    can_create_leave_request = Permission(
        "Can Create Leave Request",
        "",
        PermissionContext.FACILITY,
        employee_roles,
    )
    can_update_leave_request = Permission(
        "Can Update Leave Request",
        "",
        PermissionContext.FACILITY,
        employee_roles,
    )
    can_delete_leave_request = Permission(
        "Can Delete Leave Request",
        "",
        PermissionContext.FACILITY,
        hr_roles,
    )
    can_approve_leave_request = Permission(
        "Can Approve Leave Request",
        "",
        PermissionContext.FACILITY,
        hr_roles,
    )
    can_reject_leave_request = Permission(
        "Can Reject Leave Request",
        "",
        PermissionContext.FACILITY,
        hr_roles,
    )
    can_list_leave_types = Permission(
        "Can List Leave Types",
        "",
        PermissionContext.FACILITY,
        employee_roles,
    )
    can_create_leave_type = Permission(
        "Can Create Leave Type",
        "",
        PermissionContext.FACILITY,
        hr_roles,
    )
    can_update_leave_type = Permission(
        "Can Update Leave Type",
        "",
        PermissionContext.FACILITY,
        hr_roles,
    )
    can_delete_leave_type = Permission(
        "Can Delete Leave Type",
        "",
        PermissionContext.FACILITY,
        hr_roles,
    )
    can_list_leave_balances = Permission(
        "Can List Leave Balances",
        "",
        PermissionContext.FACILITY,
        hr_roles,
    )
    can_update_leave_balance = Permission(
        "Can Update Leave Balance",
        "",
        PermissionContext.FACILITY,
        hr_roles,
    )