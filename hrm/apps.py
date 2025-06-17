from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

PLUGIN_NAME = "hrm"

class HRMConfig(AppConfig):
   # default_auto_field = "django.db.models.BigAutoField"
   name = PLUGIN_NAME
   label = "care_plugin_hrm"
