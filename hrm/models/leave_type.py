from django.db import models
from care.emr.models import EMRBaseModel
class LeaveType(EMRBaseModel):
    name = models.CharField(max_length = 100, unique=True)
    default_days = models.PositiveIntegerField(default = 0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name