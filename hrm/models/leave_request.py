from django.db import models
from hrm.models.employee_profile import Employee
from care.emr.models import EMRBaseModel
from care.users.models import User

class LeaveRequest(EMRBaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_leaves",
    )