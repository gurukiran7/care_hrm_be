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
    requested_at: Optional[date] = None
    status: Literal["pending", "approved", "rejected", "cancelled"] = "pending"
    reason: Optional[str] = None


    @classmethod
    def perform_extra_serialization(cls, mapping, obj):
        mapping["employee"] = str(obj.employee.external_id) 
        mapping["external_id"] = str(obj.external_id)
        mapping["requested_at"] = obj.requested_at.isoformat() if obj.requested_at else None
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
        from hrm.models.leave_balance import LeaveBalance

        # Track if we need to reimburse
        was_approved = obj.status == "approved"

        if self.employee:
            obj.employee = Employee.objects.get(external_id=self.employee)
        if self.leave_type:
            obj.leave_type = LeaveType.objects.get(external_id=self.leave_type)

        # If editing an approved leave and changing to pending, reimburse balance
        if is_update and was_approved and obj.status in ["approved", "rejected"]:
            obj.status = "pending"
            balance_obj = LeaveBalance.objects.filter(employee=obj.employee, leave_type=obj.leave_type).first()
            if balance_obj:
                balance_obj.balance += obj.days_requested
                balance_obj.save()

        


class LeaveRequestRetrieveSpec(LeaveRequestBaseSpec):
    can_edit: bool = False
    can_cancel: bool = False
    leave_type: dict = None
    employee_name: str
    leave_balance: int | None = None

    @classmethod
    def perform_extra_serialization(cls, mapping, obj):
        today = date.today()
        mapping["employee"] = str(obj.employee.external_id) if obj.employee else None
        mapping["employee_name"] = (
            obj.employee.user.get_full_name()
            if obj.employee and obj.employee.user and obj.employee.user.get_full_name()
            else (obj.employee.user.username if obj.employee and obj.employee.user else "")
        )
        from hrm.models.leave_balance import LeaveBalance
        balance_obj = LeaveBalance.objects.filter(employee=obj.employee, leave_type=obj.leave_type).first()
        mapping["leave_balance"] = balance_obj.balance if balance_obj else None
        mapping["can_edit"] = (
            (obj.status == "pending") or
            (obj.status == "rejected") or
            ((obj.status == "approved") and (obj.start_date > today))
        )
        mapping["id"] = str(obj.external_id)
        mapping["can_cancel"] = (
            (obj.status == "pending") or
            ((obj.status == "approved") and (obj.start_date > today))
        )
        if obj.leave_type:
            mapping["leave_type"] = LeaveTypeRetrieveSpec.serialize(obj.leave_type).to_json()
        else:
            mapping["leave_type"] = None

class LeaveRequestListSpec(LeaveRequestRetrieveSpec):
    @classmethod
    def perform_extra_serialization(cls, mapping, obj):
        super().perform_extra_serialization(mapping, obj)
        mapping["id"] = str(obj.external_id)
