# plugin/hrm/resources/leave/spec.py

from care.emr.resources.base import EMRResource
from pydantic import UUID4, Field
from typing import Optional, Literal
from datetime import date
from hrm.models.employee_profile import Employee
from hrm.models.leave_request import LeaveRequest
from hrm.resources.employee_profile import EmployeeProfileRetrieveSpec
from hrm.resources.leave_type import LeaveTypeRetrieveSpec
from hrm.models.leave_type import LeaveType

class LeaveRequestBaseSpec(EMRResource):
    __model__ = LeaveRequest
    __exclude__ = ["employee", "leave_type"]
    id: Optional[UUID4] = None
    employee: UUID4
    leave_type: UUID4
    start_date: date
    end_date: date
    days_requested: int
    status: Literal["pending", "approved", "rejected", "cancelled"] = "pending"
    reason: Optional[str] = None

    @classmethod
    def perform_extra_serialization(cls, mapping, obj):
        mapping["employee"] = str(obj.employee.external_id) 
        mapping["external_id"] = str(obj.external_id)
        if obj.leave_type:
           mapping["leave_type"] = LeaveTypeRetrieveSpec.serialize(obj.leave_type).to_json()
        else:
           mapping["leave_type"] = None

    
class LeaveRequestCreateSpec(LeaveRequestBaseSpec):
    def perform_extra_deserialization(self, is_update, obj):
        obj.employee = Employee.objects.get(external_id=self.employee)
        obj.leave_type = LeaveType.objects.get(external_id=self.leave_type)

class LeaveRequestUpdateSpec(LeaveRequestBaseSpec):
    def perform_extra_deserialization(self, is_update, obj):
        if self.employee:
            obj.employee = Employee.objects.get(external_id=self.employee)
        if self.leave_type:
            obj.leave_type = LeaveType.objects.get(external_id=self.leave_type)
        if self.status:
            obj.status = self.status
        


class LeaveRequestRetrieveSpec(LeaveRequestBaseSpec):

    pass

class LeaveRequestListSpec(LeaveRequestRetrieveSpec):
    employee: dict
    leave_type: dict
    @classmethod
    def perform_extra_serialization(cls, mapping, obj):
        mapping["id"] = obj.external_id
        mapping["employee"] = EmployeeProfileRetrieveSpec.serialize(obj.employee).to_json()
        if obj.leave_type:
           mapping["leave_type"] = LeaveTypeRetrieveSpec.serialize(obj.leave_type).to_json()
        else:
           mapping["leave_type"] = None
