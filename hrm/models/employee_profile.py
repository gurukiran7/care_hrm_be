from django.db import models
from care.users.models import User
from care.emr.models import EMRBaseModel


class Employee(EMRBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employees")
    hire_date = models.DateField()
    address = models.TextField(default="") 
    pincode = models.IntegerField(default=0, blank=True, null=True)


    def __str__(self):
        return f"{self.user.full_name} - {self.user.user_type}"


