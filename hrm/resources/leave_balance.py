# plugin/hrm/resources/leave/spec.py
from typing import Optional
from pydantic import UUID4
from django.core.exceptions import ValidationError
from care.emr.resources.base import EMRResource
from hrm.models.leave_balance import LeaveBalance
from hrm.resources.leave_type import LeaveTypeRetrieveSpec
from django.shortcuts import get_object_or_404
from hrm.models.employee_profile import Employee  # adjust import as needed
from django.shortcuts import get_object_or_404
from hrm.models.leave_type import LeaveType  # adjust import as needed
class LeaveBalanceBaseSpec(EMRResource):
    __model__ = LeaveBalance
    __exclude__ = ["employee", "leave_type"]

    id: Optional[UUID4] = None
    employee: UUID4
    leave_type: UUID4
    balance: int| None = None

    @classmethod
    def perform_extra_serialization(cls, mapping, obj):
        mapping["leave_type"] =  obj.leave_type.name if obj.leave_type else None

class LeaveBalanceCreateSpec(LeaveBalanceBaseSpec):
    employee: UUID4
    leave_type: UUID4
    balance: int = 0

    def perform_extra_deserialization(self, is_update, obj):
        # Convert UUIDs to model instances
        if self.employee:
            obj.employee = get_object_or_404(Employee, external_id=self.employee)
        if self.leave_type:
            obj.leave_type = get_object_or_404(LeaveType, external_id=self.leave_type)

        if not is_update:
         if LeaveBalance.objects.filter(employee=obj.employee, leave_type=obj.leave_type).exists():
            raise ValidationError("LeaveBalance for this employee and leave type already exists.")

class LeaveBalanceUpdateSpec(LeaveBalanceBaseSpec):
    leave_type: UUID4 | None = None
    employee: UUID4 | None = None
    

class LeaveBalanceRetrieveSpec(LeaveBalanceBaseSpec):
    pass

class LeaveBalanceListSpec(LeaveBalanceRetrieveSpec):
    leave_type:str
    external_id: str
    employee: str

    @classmethod
    def perform_extra_serialization(cls, mapping, obj):
        mapping["employee"]= str(obj.employee.external_id) if obj.employee else None
        mapping["external_id"] = str(obj.external_id)
        mapping["leave_type"] =  obj.leave_type.name if obj.leave_type else None