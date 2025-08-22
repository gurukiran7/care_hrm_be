from care.security.authorization.base import AuthorizationHandler, AuthorizationController
from hrm.security.permissions.holiday import HolidayPermissions

class HolidayAccess(AuthorizationHandler):
    def can_list_holidays(self, user):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [HolidayPermissions.can_list_holidays.name], user
        ) or self.check_permission_in_organization(
            [HolidayPermissions.can_list_holidays.name], user
        )

    def can_create_holiday(self, user):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [HolidayPermissions.can_create_holiday.name], user
        ) or self.check_permission_in_organization(
            [HolidayPermissions.can_create_holiday.name], user
        )

    def can_update_holiday(self, user, holiday):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [HolidayPermissions.can_update_holiday.name], user
        ) or self.check_permission_in_organization(
            [HolidayPermissions.can_update_holiday.name], user
        )

    def can_delete_holiday(self, user, holiday):
        if user.is_superuser:
            return True
        return self.check_permission_in_facility_organization(
            [HolidayPermissions.can_delete_holiday.name], user
        ) or self.check_permission_in_organization(
            [HolidayPermissions.can_delete_holiday.name], user
        )

AuthorizationController.register_internal_controller(HolidayAccess)