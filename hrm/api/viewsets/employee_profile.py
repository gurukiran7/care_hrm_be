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
from hrm.models.holiday import Holiday
from hrm.models.leave_request import LeaveRequest
from care.security.authorization import AuthorizationController
from rest_framework.exceptions import PermissionDenied

class EmployeeProfileFilters(filters.FilterSet):
    user = filters.UUIDFilter(field_name="user__external_id")
    first_name = filters.CharFilter(field_name="user__first_name", lookup_expr="icontains")


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

    def authorize_list(self):
        if self.request.user.is_superuser:
            return
        if not AuthorizationController.call(
            "can_list_employees", self.request.user
        ):
            raise PermissionDenied("You do not have permission to list employees.")

    def authorize_retrieve(self, model_instance):
        if self.request.user.is_superuser:
             return
        if AuthorizationController.call(
            "can_view_employee_details", self.request.user, model_instance
        ):
            return
        if AuthorizationController.call(
            "can_view_own_employee_profile", self.request.user, model_instance
        ):
             return
        raise PermissionDenied("You do not have permission to view this employee profile.")
    def authorize_update(self, model_instance, request_obj):
        if self.request.user.is_superuser:
            return
        if not AuthorizationController.call(
            "can_update_employee", self.request.user, model_instance
        ):
            raise PermissionDenied("You do not have permission to update this employee profile.")

    def authorize_create(self):
        if self.request.user.is_superuser:
            return
        if not AuthorizationController.call(
            "can_create_employee", self.request.user
        ):
            raise PermissionDenied("You do not have permission to create employee profiles.")

    @action(detail=False, methods=["GET"], url_path="current")
    def get_current_employee(self, request):
        if request.user.is_superuser:
           return Response(None, status=200)
        employee = Employee.objects.filter(user=request.user).first()
        if not employee:
           return Response({"detail": "Employee record not found."}, status=404)
        data = self.pydantic_retrieve_model.serialize(employee).to_json()
        return Response(data)

    @action(detail=True, methods=["GET"], url_path="holidays")
    def get_employee_holidays(self, request, pk=None, **kwargs):
        employee = self.get_object()
        today = date.today()
        holidays = Holiday.objects.filter(deleted=False, date__gte=today)
        leaves = LeaveRequest.objects.filter(employee=employee, status="approved", end_date__gte=today)
        result = []
        for holiday in holidays:
            result.append({
                "id": holiday.id, 
                "type": "holiday",
                "name": holiday.name,
                "date": holiday.date,
                "description": holiday.description,
            })
        for leave in leaves:
            result.append({
                "id": leave.id, 
                "type": "leave",
                "name": leave.leave_type.name if leave.leave_type else "Leave",
                "start_date": leave.start_date,
                "end_date": leave.end_date,
                "reason": leave.reason,
            })
        return Response(result)

