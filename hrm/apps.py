from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

PLUGIN_NAME = "hrm"


class HRMConfig(AppConfig):
    name = PLUGIN_NAME
    verbose_name = _("Hello")
