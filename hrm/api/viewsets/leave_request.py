from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from care.emr.api.viewsets.base import (
    EMRBaseViewSet,
    EMRCreateMixin,
    EMRListMixin,
    EMRRetrieveMixin,
    EMRUpdateMixin,
)
from hrm.models.leave_request import LeaveRequest
from hrm.models.employee_profile import Employee
from hrm.resources.leave_request import (
    LeaveRequestCreateSpec,
    LeaveRequestUpdateSpec,
    LeaveRequestRetrieveSpec,
    LeaveRequestListSpec,
)
from datetime import datetime
from care.security.authorization import AuthorizationController
from rest_framework.exceptions import PermissionDenied
from datetime import date
from hrm.models.leave_type import LeaveType
from hrm.models.leave_balance import LeaveBalance

class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass
class LeaveRequestFilters(filters.FilterSet):
    employee = filters.UUIDFilter(field_name="employee__external_id")
    status = CharInFilter(field_name="status", lookup_expr="in")
    start_date = filters.DateFilter(field_name="start_date", lookup_expr="gt")
    end_date = filters.DateFilter(field_name="end_date", lookup_expr="gte")

class LeaveRequestViewSet(EMRCreateMixin, EMRRetrieveMixin, EMRUpdateMixin, EMRListMixin, EMRBaseViewSet):
    database_model = LeaveRequest
    pydantic_model = LeaveRequestCreateSpec
    pydantic_update_model = LeaveRequestUpdateSpec
    pydantic_read_model = LeaveRequestListSpec
    pydantic_retrieve_model = LeaveRequestRetrieveSpec
    filterset_class = LeaveRequestFilters
    filter_backends = [filters.DjangoFilterBackend]

    def authorize_update(self, request_obj, model_instance):
        if not AuthorizationController.call(
            "can_update_leave_request", self.request.user, model_instance
        ):
            raise PermissionDenied("You do not have permission to update leave requests.")

    # def authorize_create(self, request_obj):
    #     if not AuthorizationController.call(
    #         "can_create_leave_request", self.request.user
    #     ):
    #         raise PermissionDenied("You do not have permission to create leave requests.")

    def authorize_list(self, request_obj):
        if self.request.user.is_superuser:
            return
        if not AuthorizationController.call(
            "can_list_leave_requests", self.request.user
        ):
            raise PermissionDenied("You do not have permission to list leave requests.")

    @action(detail=True, methods=["POST"])
    def approve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status in ["cancelled"]:
            return Response({"detail": f"Cannot approve a leave request that is {instance.status}."}, status=status.HTTP_400_BAD_REQUEST)
        if not AuthorizationController.call(
            "can_approve_leave_request", self.request.user, instance
        ):
            raise PermissionDenied("You do not have permission to approve leave requests.")

        balance = LeaveBalance.objects.get(employee=instance.employee, leave_type=instance.leave_type)
        if balance.balance < instance.days_requested:
            return Response({"detail": "Insufficient leave balance."}, status=status.HTTP_400_BAD_REQUEST)

        instance.status = "approved"
        instance.approved_by = self.request.user
        instance.save()
        return Response({}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def reject(self, request, *args, **kwargs):
        instance = self.get_object()
        if not AuthorizationController.call(
            "can_reject_leave_request", self.request.user, instance
        ):
            raise PermissionDenied("You do not have permission to reject leave requests.")
        instance.status = "rejected"
        instance.approved_by = self.request.user
        instance.save()
        return Response({}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def cancel(self, request, *args, **kwargs):
        instance = self.get_object()
        today = date.today()
        if today >= instance.start_date:
            return Response({"detail": "Cannot cancel leave after it has started."}, status=status.HTTP_400_BAD_REQUEST)
        if instance.status in ["pending"]:
            instance.status = "cancelled"
            instance.save()
            return Response({"detail": "Leave cancelled."}, status=status.HTTP_200_OK)
        elif instance.status == "approved":
            instance.status = "cancellation_requested"
            instance.save()
            return Response({"detail": "Cancellation requested. Awaiting HR approval."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Cannot cancel leave in current status."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"])
    def approve_cancellation(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != "cancellation_requested":
            return Response({"detail": "No cancellation request pending."}, status=status.HTTP_400_BAD_REQUEST)
        balance = LeaveBalance.objects.get(employee=instance.employee, leave_type=instance.leave_type)
        balance.balance += instance.days_requested
        balance.save()
        instance.status = "cancelled"
        instance.save()
        return Response({"detail": "Cancellation approved and leave balance reimbursed."}, status=status.HTTP_200_OK)


