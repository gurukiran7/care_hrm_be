from care.security.authorization.base import AuthorizationHandler, AuthorizationController
from hrm.security.permissions.leave import LeavePermissions

class LeaveAccess(AuthorizationHandler):
    def can_list_leave_requests(self, user):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [LeavePermissions.can_list_leave_requests.name], user
        ) or self.check_permission_in_organization(
            [LeavePermissions.can_list_leave_requests.name], user
        )

    def can_create_leave_request(self, user):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [LeavePermissions.can_create_leave_request.name], user
        ) or self.check_permission_in_organization(
            [LeavePermissions.can_create_leave_request.name], user
        )

    def can_update_leave_request(self, user, leave_request):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [LeavePermissions.can_update_leave_request.name], user
        ) or self.check_permission_in_organization(
            [LeavePermissions.can_update_leave_request.name], user
        )

    def can_delete_leave_request(self, user, leave_request):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [LeavePermissions.can_delete_leave_request.name], user
        ) or self.check_permission_in_organization(
            [LeavePermissions.can_delete_leave_request.name], user
        )

    def can_approve_leave_request(self, user, leave_request):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [LeavePermissions.can_approve_leave_request.name], user
        ) or self.check_permission_in_organization(
            [LeavePermissions.can_approve_leave_request.name], user
        )

    def can_reject_leave_request(self, user, leave_request):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [LeavePermissions.can_reject_leave_request.name], user
        ) or self.check_permission_in_organization(
            [LeavePermissions.can_reject_leave_request.name], user
        )

    def can_list_leave_types(self, user):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [LeavePermissions.can_list_leave_types.name], user
        ) or self.check_permission_in_organization(
            [LeavePermissions.can_list_leave_types.name], user
        )

    def can_create_leave_type(self, user):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [LeavePermissions.can_create_leave_type.name], user
        ) or self.check_permission_in_organization(
            [LeavePermissions.can_create_leave_type.name], user
        )

    def can_update_leave_type(self, user, leave_type):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [LeavePermissions.can_update_leave_type.name], user
        ) or self.check_permission_in_organization(
            [LeavePermissions.can_update_leave_type.name], user
        )

    def can_delete_leave_type(self, user, leave_type):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [LeavePermissions.can_delete_leave_type.name], user
        ) or self.check_permission_in_organization(
            [LeavePermissions.can_delete_leave_type.name], user
        )

    def can_list_leave_balances(self, user):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [LeavePermissions.can_list_leave_balances.name], user
        ) or self.check_permission_in_organization(
            [LeavePermissions.can_list_leave_balances.name], user
        )

    def can_update_leave_balance(self, user, leave_balance):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [LeavePermissions.can_update_leave_balance.name], user
        ) or self.check_permission_in_organization(
            [LeavePermissions.can_update_leave_balance.name], user
        )
AuthorizationController.register_internal_controller(LeaveAccess)