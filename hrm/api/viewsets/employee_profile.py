from datetime import datetime
from django.db import transaction
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
import csv
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

    @action(detail=False, methods=["GET"], url_path="export")
    def export(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=employees.csv"
        writer = csv.writer(response)
        writer.writerow(["Full Name", "Email", "Department", "Role", "Hire Date", "Phone Number"])
        for employee in self.get_queryset():
            writer.writerow({
                employee.user.get_full_name() or employee.user.username,
                employee.user.email,
                employee.department,
                employee.role,
                employee.hire_date,
                employee.user.phone_number 
            })

        return response