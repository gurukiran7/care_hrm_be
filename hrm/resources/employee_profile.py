from pydantic import BaseModel, Field, UUID4, StrictStr, field_validator
from care.emr.resources.base import EMRResource
from care.users.models import User, Skill
from datetime import date, datetime
from hrm.models.employee_profile import Employee
from care.emr.resources.user.spec import UserCreateSpec, UserRetrieveSpec, UserUpdateSpec
from hrm.signals import suppress_employee_signal
from typing import List, Optional
from care.emr.models import Organization
from care.emr.models.organization import OrganizationUser
from care.security.models import RoleModel
from care.emr.resources.user.spec import UserTypeRoleMapping

class UserWithExtrasMixin:
    date_of_birth: Optional[date] = None
    weekly_working_hours: Optional[int] = None
    qualification: Optional[str] = None
    skills: Optional[List[UUID4]] = None



class UserCreateWithExtras(UserWithExtrasMixin, UserCreateSpec):
    pass


class UserUpdateWithExtras(UserWithExtrasMixin, UserUpdateSpec):
    pass

class EmployeeProfileBaseSpec(EMRResource):
    __model__ = Employee
    __exclude__= ["user"]

    id: UUID4 | None = None
    user: UserCreateWithExtras | None = None
    hire_date: date
    address: Optional[str] = None
    pincode: Optional[int] = None

    @field_validator("hire_date")
    def validate_hire_date(cls, hire_date):
        from datetime import date
        if hire_date > date.today():
            raise ValueError("Hire date cannot be in the future.")
        return hire_date

    def _apply_common_fields(self, obj):
        """Helper to set common Employee fields."""
        if self.hire_date is not None:
            obj.hire_date = self.hire_date
        if self.address is not None:
            obj.address = self.address
        if self.pincode is not None:
            obj.pincode = self.pincode

    def _handle_user_skills(self, user_instance, skills):
        """Helper to handle M2M skills update."""
        if skills is not None:
            skill_objs = Skill.objects.filter(external_id__in=skills)
            user_instance.skills.set(skill_objs)


class EmployeeProfileCreateSpec(EmployeeProfileBaseSpec):
    user: UserCreateWithExtras

    def perform_extra_deserialization(self, is_update, obj, request=None):
        if not is_update:
            with suppress_employee_signal():
                user_data = self.user.model_dump(exclude={"id", "meta", "skills"})
                if request and request.user.is_authenticated:
                    user_data["created_by"] = request.user
                user_instance = User.objects.create_user(**user_data)
                self._handle_user_skills(user_instance, self.user.skills)
            obj.user = user_instance

            org_name = user_instance.user_type.capitalize()
            org = Organization.objects.filter(
                parent__isnull=True,
                name=org_name,
                org_type="role",
                system_generated=True,
            ).first()
            if not org:
                org = Organization.objects.create(
                    name=org_name, org_type="role", system_generated=True
                )
            OrganizationUser.objects.create(
                organization=org,
                user=user_instance,
                role=RoleModel.objects.get(
                    is_system=True,
                    name=UserTypeRoleMapping[user_instance.user_type].value.name,
                ),
            )

        self._apply_common_fields(obj)
        obj.save()

class EmployeeProfileUpdateSpec(EmployeeProfileBaseSpec):
    hire_date: date | None = None
    user: UserUpdateWithExtras | None = None

    def perform_extra_deserialization(self, is_update, obj):
        self._apply_common_fields(obj)

        if self.user and obj.user:
            user_instance = obj.user
            user_data = self.user.model_dump(
                exclude_unset=True, exclude={"id", "meta", "skills"}
            )
            for field, value in user_data.items():
                setattr(user_instance, field, value)

            self.user.perform_extra_deserialization(is_update=True, obj=user_instance)
            self._handle_user_skills(user_instance, self.user.skills)
            user_instance.save()

class EmployeeProfileListSpec(EmployeeProfileBaseSpec):
    user: dict | None = None
    is_on_leave: bool = False

    @classmethod
    def perform_extra_serialization(cls, mapping, obj):
        super().perform_extra_serialization(mapping, obj)
        mapping["user"] = UserRetrieveSpec.serialize(obj.user).to_json() if obj.user else None
        mapping["is_on_leave"] = getattr(obj, "is_on_leave", False)

class EmployeeProfileRetrieveSpec(EmployeeProfileListSpec):
    permissions: list = []

    @classmethod
    def perform_extra_serialization(cls, mapping, obj):
        super().perform_extra_serialization(mapping, obj)

        if obj.user:
            user_data = UserRetrieveSpec.serialize(obj.user).to_json()
            user_data["date_of_birth"] = obj.user.date_of_birth
            user_data["weekly_working_hours"] = obj.user.weekly_working_hours
            user_data["skills"] = list(
                obj.user.skills.values("external_id", "name", "description")
            )
            user_data["qualification"] = obj.user.qualification
            mapping["user"] = user_data

            # Add permissions
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
