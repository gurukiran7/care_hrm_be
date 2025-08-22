from django.db import models
from care.emr.models import EMRBaseModel

class Holiday(EMRBaseModel):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.date})"