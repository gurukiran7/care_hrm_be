from django.db import models
from care.users.models import User
from care.emr.models import EMRBaseModel


class Employee(EMRBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employees")
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.user.full_name} - {self.role}"


