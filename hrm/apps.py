from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from care.security.permissions.base import PermissionController


PLUGIN_NAME = "hrm"

class HRMConfig(AppConfig):
   # default_auto_field = "django.db.models.BigAutoField"
   name = PLUGIN_NAME
   label = "care_plugin_hrm"
   def ready(self):
      import hrm.signals
      import hrm.security.authorization.leave
      from hrm.security.permissions.leave import LeavePermissions
      PermissionController.register_permission_handler(LeavePermissions)

       