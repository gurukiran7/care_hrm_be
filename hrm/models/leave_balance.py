from care.emr.models import EMRBaseModel
from hrm.models.leave_type import LeaveType
from hrm.models.employee_profile import Employee
from django.db import models

class LeaveBalance(EMRBaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leave_balances")
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name="leave_balances")
    balance = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (("employee", "leave_type"))