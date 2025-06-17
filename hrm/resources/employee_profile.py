from pydantic import BaseModel, Field, UUID4, StrictStr, field_validator
from care.emr.resources.base import EMRResource
from care.users.models import User 
from datetime import date , datetime
from hrm.models.employee_profile import Employee
from care.emr.resources.user.spec import UserCreateSpec, UserRetrieveSpec

class EmployeeProfileBaseSpec(EMRResource):
    __model__ = Employee

    id: UUID4 | None = None
    user: UserRetrieveSpec
    department: StrictStr = Field(max_length = 100)
    role: StrictStr = Field(max_length = 100)
    hire_date: date
    created_date: datetime
    modified_date: datetime


    @field_validator("hire_date")
    def validate_hire_date(cls, hire_date):
        from datetime import date
        if hire_date > date.today():
            raise ValueError("Hire date cannot be in the future.")
        return hire_date

class EmployeeProfileCreateSpec(EmployeeProfileBaseSpec):
    user_id: UUID4
    user: UserCreateSpec

    @classmethod
    def validate_user_id(cls, user_id):
        if not User.objects.filter(external_id=user_id).exists():
            raise ValueError("User does not exist")
        return user_id

    def perform_extra_deserialization(self, is_update, obj):
        obj.user = User.objects.get(external_id=self.user_id)


class EmployeeProfileUpdateSpec(EmployeeProfileBaseSpec):
    department: str | None = None
    role: str | None = None
    hire_date: date | None = None


class EmployeeProfileRetrieveSpec(EmployeeProfileBaseSpec):
    user_details: dict | None = None

    @classmethod
    def perform_extra_serialization(cls, mapping, obj):
        super().perform_extra_serialization(mapping, obj)
        mapping["user_details"] = UserRetrieveSpec.serialize(obj.user).to_json()
