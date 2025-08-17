from pydantic import BaseModel, Field, UUID4, StrictStr, field_validator
from care.emr.resources.base import EMRResource
from care.users.models import User 
from datetime import date, datetime
from hrm.models.employee_profile import Employee
from care.emr.resources.user.spec import UserCreateSpec, UserRetrieveSpec, UserUpdateSpec
from hrm.signals import suppress_employee_signal
from typing import List, Optional

class EmployeeProfileBaseSpec(EMRResource):
    __model__ = Employee
    __exclude__= ["user"]

    id: UUID4 | None = None
    user: UserCreateSpec | None = None
    hire_date: date
    address: Optional[str] = None  
    education: Optional[str] = None  # <-- Now a string field
    pincode: Optional[int] = None 

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
        obj.hire_date = self.hire_date
        obj.address = self.address  
        obj.education = self.education  
        obj.pincode = self.pincode 
        obj.save() 

class EmployeeProfileUpdateSpec(EmployeeProfileBaseSpec):
    hire_date: date | None = None
    user: UserUpdateSpec | None = None
    address: Optional[str] = None
    education: Optional[str] = None  
    pincode: Optional[int] = None  

    def perform_extra_deserialization(self, is_update, obj):
        if self.hire_date is not None:
            obj.hire_date = self.hire_date

        if self.user is not None and obj.user is not None:
            user_instance = obj.user
            user_data = self.user.model_dump(exclude_unset=True, exclude={"id", "meta"})
            for field, value in user_data.items():
                setattr(user_instance, field, value)
            self.user.perform_extra_deserialization(is_update=True, obj=user_instance)
            user_instance.save()

        if self.address is not None:
            obj.address = self.address

        if self.education is not None:
            obj.education = self.education 

        if self.pincode is not None:  
            obj.pincode = self.pincode

class EmployeeProfileListSpec(EmployeeProfileBaseSpec):
    user: dict | None = None
    is_on_leave: bool = False  

    @classmethod
    def perform_extra_serialization(cls, mapping, obj):
        super().perform_extra_serialization(mapping, obj)
        mapping["user"] = UserRetrieveSpec.serialize(obj.user).to_json() if obj.user else None
        mapping["is_on_leave"] = getattr(obj, "is_on_leave", False)
        mapping["pincode"] = obj.pincode  
        mapping["education"] = obj.education  

class EmployeeProfileRetrieveSpec(EmployeeProfileListSpec):
    permissions: list = []

    @classmethod
    def perform_extra_serialization(cls, mapping, obj):
        super().perform_extra_serialization(mapping, obj)
        mapping["address"] = obj.address
        mapping["pincode"] = obj.pincode  
        mapping["education"] = obj.education  

        if obj.user:
            from care.security.models import RolePermission
            from care.emr.models.organization import OrganizationUser
            permissions = RolePermission.objects.filter(
                role_id__in=OrganizationUser.objects.filter(user=obj.user).values_list(
                    "role_id", flat=True
                )
            ).select_related("permission")
            mapping["permissions"] = [perm.permission.slug for perm in permissions]
        else:
            mapping["permissions"] = []
