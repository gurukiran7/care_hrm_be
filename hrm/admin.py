from django.contrib import admin
from hrm.models.employee_profile import Employee
from hrm.models.leave_type import LeaveType
from hrm.models.leave_balance import LeaveBalance
from hrm.models.leave_request import LeaveRequest

admin.site.register(Employee)
admin.site.register(LeaveType)
admin.site.register(LeaveBalance)
admin.site.register(LeaveRequest)