from django.db import models
from hrm.models.employee_profile import Employee
from care.emr.models import EMRBaseModel
from care.users.models import User
from hrm.models.leave_type import LeaveType
from hrm.models.leave_balance import LeaveBalance


class LeaveRequest(EMRBaseModel):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
        
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    days_requested = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    reason = models.TextField(blank=True, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,related_name="reviewed_leave_requests")


    def save(self, *args, **kwargs):
        is_new = self._state.adding
        deduct_balance = False
        if is_new and self.status == "approved":
            deduct_balance = True
        elif not is_new:
            old = LeaveRequest.objects.get(pk=self.pk)
            if old.status != "approved" and self.status == "approved":
                deduct_balance = True
        if deduct_balance:
            balance = LeaveBalance.objects.get(employee=self.employee, leave_type=self.leave_type)
            if balance.balance < self.days_requested:
                raise ValueError("Insufficient leave balance")
            balance.balance -=self.days_requested
            balance.save()
        super().save(*args, **kwargs)   

