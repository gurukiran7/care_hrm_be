from pydantic import BaseModel, Field, UUID4, StrictStr, field_validator
from care.emr.resources.base import EMRResource
from care.users.models import User 
from datetime import date , datetime
from hrm.models.employee_profile import Employee
from care.emr.resources.user.spec import UserCreateSpec, UserRetrieveSpec, UserUpdateSpec
from hrm.signals import suppress_employee_signal

class EmployeeProfileBaseSpec(EMRResource):
    __model__ = Employee
    __exclude__= ["user"]

    id: UUID4 | None = None
    user: UserCreateSpec | None = None
    department: str = Field(max_length = 100)
    role: str = Field(max_length = 100)
    hire_date: date

    @field_validator("hire_date")
    def validate_hire_date(cls, hire_date):
        from datetime import date
        if hire_date > date.today():
            raise ValueError("Hire date cannot be in the future.")
        return hire_date

class EmployeeProfileCreateSpec(EmployeeProfileBaseSpec):
    user: UserCreateSpec

    def perform_extra_deserialization(self, is_update, obj, request=None):
        if not is_update:
            with suppress_employee_signal():
                user_data = self.user.model_dump(exclude={"id", "meta"})
                if request and request.user.is_authenticated:
                    user_data["created_by"] = request.user
                user_instance = User.objects.create_user(**user_data)
            obj.user = user_instance
        obj.department = self.department
        obj.role = self.role
        obj.hire_date = self.hire_date



class EmployeeProfileUpdateSpec(EmployeeProfileBaseSpec):
    department: str | None = None
    role: str | None = None
    hire_date: date | None = None
    user: UserUpdateSpec | None = None

    def perform_extra_deserialization(self, is_update, obj):
        # Update Employee fields
        if self.department is not None:
            obj.department = self.department
        if self.role is not None:
            obj.role = self.role
        if self.hire_date is not None:
            obj.hire_date = self.hire_date

        if self.user is not None and obj.user is not None:
           user_instance = obj.user
           user_data = self.user.model_dump(exclude_unset=True, exclude={"id", "meta"})
           for field, value in user_data.items():
               setattr(user_instance, field, value)
           self.user.perform_extra_deserialization(is_update=True, obj=user_instance)
           user_instance.save()



class EmployeeProfileRetrieveSpec(EmployeeProfileBaseSpec):
    user_details: dict | None = None

    @classmethod
    def perform_extra_serialization(cls, mapping, obj):
        super().perform_extra_serialization(mapping, obj)
        mapping["user_details"] = UserRetrieveSpec.serialize(obj.user).to_json()
