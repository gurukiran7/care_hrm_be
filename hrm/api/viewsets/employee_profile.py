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
    EmployeeProfileListSpec
)
from datetime import date
from django.db.models import OuterRef, Exists  

class EmployeeProfileFilters(filters.FilterSet):
    department = filters.CharFilter(field_name="department", lookup_expr="icontains")
    role = filters.CharFilter(field_name="role", lookup_expr="icontains")
    user = filters.UUIDFilter(field_name="user__external_id")


class EmployeeProfileViewSet( EMRCreateMixin, EMRRetrieveMixin, EMRUpdateMixin, EMRListMixin, EMRBaseViewSet):
    database_model = Employee
    pydantic_model = EmployeeProfileCreateSpec
    pydantic_update_model = EmployeeProfileUpdateSpec
    pydantic_read_model = EmployeeProfileListSpec
    pydantic_retrieve_model = EmployeeProfileRetrieveSpec
    filterset_class = EmployeeProfileFilters
    filter_backends = [filters.DjangoFilterBackend]

    def create(self, request, *args, **kwargs):
        instance = self.pydantic_model(**request.data)
        obj = self.database_model()
        instance.perform_extra_deserialization(is_update=False, obj=obj, request=request)
        obj.save()
        return Response(self.pydantic_retrieve_model.serialize(obj).to_json())

    def get_queryset(self):
        today = date.today()
        from hrm.models.leave_request import LeaveRequest

        leave_subquery = LeaveRequest.objects.filter(
            employee=OuterRef('pk'),
            status="approved",
            start_date__lte=today,
            end_date__gte=today,
        )
        return (
            super()
            .get_queryset()
            .select_related("user")
            .annotate(is_on_leave=Exists(leave_subquery))
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
    
    @action(detail=False, methods=["GET"], url_path="current")
    def get_current_employee(self, request):
        if request.user.is_superuser:
           return Response(None, status=200)
        employee = Employee.objects.filter(user=request.user).first()
        if not employee:
           return Response({"detail": "Employee record not found."}, status=404)
        data = self.pydantic_retrieve_model.serialize(employee).to_json()
        return Response(data)

   