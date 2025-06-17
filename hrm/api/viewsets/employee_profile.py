from datetime import datetime
from django.db import transaction
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from care.emr.api.viewsets.base import (
    EMRBaseViewSet,
    EMRCreateMixin,
    EMRListMixin,
    EMRRetrieveMixin,
    EMRUpdateMixin,
)
from care.users.models import User
from hrm.models.employee_profile import Employee
from hrm.resources.employee_profile import (
    EmployeeProfileCreateSpec,
    EmployeeProfileUpdateSpec,
    EmployeeProfileRetrieveSpec,
    EmployeeProfileBaseSpec,
)

class EmployeeProfileFilters(filters.FilterSet):
    department = filters.CharFilter(field_name="department", lookup_expr="icontains")
    role = filters.CharFilter(field_name="role", lookup_expr="icontains")
    user = filters.UUIDFilter(field_name="user__external_id")


class EmployeeProfileViewSet( EMRCreateMixin, EMRRetrieveMixin, EMRUpdateMixin, EMRListMixin, EMRBaseViewSet):
    database_model = Employee
    pydantic_model = EmployeeProfileCreateSpec
    pydantic_update_model = EmployeeProfileUpdateSpec
    pydantic_read_model = EmployeeProfileBaseSpec
    pydantic_retrieve_model = EmployeeProfileRetrieveSpec
    filterset_class = EmployeeProfileFilters
    filter_backends = [filters.DjangoFilterBackend]


    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("user")
            .order_by("-created_date")
        )
    
    def perform_create(self, instance):
        with transaction.atomic():
            # Check if Employee already exists for the User (by email or username)
            if Employee.objects.filter(user__email=instance.user.email).exists():
                raise ValidationError("Employee for this User already exists")
            instance.user.save()
            super().perform_create(instance)

    @action(detail=False, methods=["POST"])
    def auto_create_for_existing_users(self, request):
        with transaction.atomic():
            created = 0
            users_without_employee = User.objects.filter(
                deleted=False, is_superuser = False
            ).exclude(id__in=Employee.objects.values_list("user", flat=True))
            for user in users_without_employee:
                Employee.objects.create(
                    user=user,
                    department="Unknown",
                    role="Unknown",
                    hire_date=datetime.today().date(),
                )
                created += 1
            return Response({"created": created})