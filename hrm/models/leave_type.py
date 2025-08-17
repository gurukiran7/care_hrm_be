from django.db import models
from care.emr.models import EMRBaseModel
class LeaveType(EMRBaseModel):
    name = models.CharField(max_length = 100)
    default_days = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.name