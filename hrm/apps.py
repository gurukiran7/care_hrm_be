from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from care.security.permissions.base import PermissionController


PLUGIN_NAME = "hrm"

class HRMConfig(AppConfig):
   name = PLUGIN_NAME
   label = "care_plugin_hrm"
   def ready(self):
      import hrm.signals
      import hrm.security.authorization.leave
      import hrm.security.authorization.employee 
      import hrm.security.authorization.holiday  
      from hrm.security.permissions.leave import LeavePermissions
      from hrm.security.permissions.employee import EmployeePermissions
      from hrm.security.permissions.holiday import HolidayPermissions 
      PermissionController.register_permission_handler(LeavePermissions)
      PermissionController.register_permission_handler(EmployeePermissions)
      PermissionController.register_permission_handler(HolidayPermissions) 

