from care.security.authorization.base import AuthorizationHandler, AuthorizationController
from hrm.security.permissions.employee import EmployeePermissions

class EmployeeAccess(AuthorizationHandler):
    def can_list_employees(self, user):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [EmployeePermissions.can_list_employees.name], user
        ) or self.check_permission_in_organization(
            [EmployeePermissions.can_list_employees.name], user
        )

    def can_create_employee(self, user):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [EmployeePermissions.can_create_employee.name], user
        ) or self.check_permission_in_organization(
            [EmployeePermissions.can_create_employee.name], user
        )

    def can_update_employee(self, user, employee):
        if user.is_superuser:
            return True
        if self.check_permission_in_facility_organization(
            [EmployeePermissions.can_update_employee.name], user
        ) or self.check_permission_in_organization(
            [EmployeePermissions.can_update_employee.name], user
        ):
            return True

    def can_view_employee_details(self, user, employee):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [EmployeePermissions.can_view_employee_details.name], user
        ) or self.check_permission_in_organization(
            [EmployeePermissions.can_view_employee_details.name], user
        )

    def can_view_own_employee_profile(self, user, employee):
        if user.is_superuser:
            return True
        print("employee.user.id:", getattr(employee.user, "id", None), "user.id:", getattr(user, "id", None))
        return (
            self.check_permission_in_facility_organization(
                [EmployeePermissions.can_view_own_employee_profile.name], user
            )
            or self.check_permission_in_organization(
                [EmployeePermissions.can_view_own_employee_profile.name], user
            )
        ) and getattr(employee.user, "id", None) == getattr(user, "id", None)

AuthorizationController.register_internal_controller(EmployeeAccess)