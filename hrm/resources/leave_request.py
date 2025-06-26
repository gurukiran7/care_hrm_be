from datetime import datetime, date
from pydantic import UUID4, Field, field_validator, model_validator
from care.emr.resources.base import EMRResource
from hrm.models.leave_request import LeaveRequest, Employee
from hrm.resources.employee_profile import EmployeeProfileRetrieveSpec

class LeaveRequestBaseSpec(EMRResource):
    __model__ = LeaveRequest

    id: UUID4 | None = None
    employee_id: UUID4
    leave_type: str = Field(max_length=50)
    start_date: date
    end_date: date
    reason: str = Field(max_length=255)
    status: str = Field(default="pending", max_length=20)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("End date cannot be earlier than start date")
        return self

    @field_validator("employee_id")
    @classmethod
    def validate_employee(cls, employee):
        if not Employee.objects.filter(external_id=employee).exists():
            raise ValueError("Employee does not exist")
        return employee


class LeaveRequestCreateSpec(LeaveRequestBaseSpec):
    def perform_extra_deserialization(self, is_update, obj):
        obj.employee = Employee.objects.get(external_id=self.employee_id)


class LeaveRequestUpdateSpec(LeaveRequestBaseSpec):
    status: str = Field(default=None, max_length=20)


class LeaveRequestListSpec(LeaveRequestBaseSpec):
    employee: dict
    created_date: datetime
    modified_date: datetime

    @classmethod
    def perform_extra_serialization(cls, mapping, obj):
        mapping["id"] = obj.external_id
        mapping["employee"] = EmployeeProfileRetrieveSpec.serialize(obj.employee).to_json()


class LeaveRequestRetrieveSpec(LeaveRequestListSpec):
    approved_by: dict | None = None

    @classmethod
    def perform_extra_serialization(cls, mapping, obj):
        super().perform_extra_serialization(mapping, obj)
        if obj.approved_by:
            from care.emr.resources.user.spec import UserRetrieveSpec
            mapping["approved_by"] = UserRetrieveSpec.serialize(obj.approved_by).to_json()
