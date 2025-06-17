from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

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

class LeaveRequestFilters(filters.FilterSet):
    employee = filters.UUIDFilter(field_name="employee__external_id")
    status = filters.CharFilter(field_name="status", lookup_expr="iexact")

class LeaveRequestViewSet(EMRCreateMixin, EMRRetrieveMixin, EMRUpdateMixin, EMRListMixin, EMRBaseViewSet):
    database_model = LeaveRequest
    pydantic_model = LeaveRequestCreateSpec
    pydantic_update_model = LeaveRequestUpdateSpec
    pydantic_read_model = LeaveRequestListSpec
    pydantic_retrieve_model = LeaveRequestRetrieveSpec
    filterset_class = LeaveRequestFilters
    filter_backends = [filters.DjangoFilterBackend]

    def authorize_create(self, instance):
        employee = get_object_or_404(Employee, external_id=instance.employee_id)
        if self.request.user != employee.user and not self.request.user.is_staff:
            raise PermissionDenied("Only the employee or HR can submit leave requests")

    def authorize_update(self, request_obj, model_instance):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only HR can approve/reject leave requests")

    def perform_update(self, instance):
        with transaction.atomic():
            if self.request.data.get("status") in ["approved", "rejected"]:
                instance.approved_by = self.request.user
                instance.modified_date = datetime.datetime.now()
            super().perform_update(instance)


    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("employee", "employee__user", "approved_by")
            .order_by("-created_date")
        )


    @action(detail=True, methods=["POST"])
    def approve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.authorize_update({}, instance)
        instance.status = "approved"
        instance.approved_by = self.request.user
        instance.save()
        return Response({}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def reject(self, request, *args, **kwargs):
        instance = self.get_object()
        self.authorize_update({}, instance)
        instance.status = "rejected"
        instance.approved_by = self.request.user
        instance.save()
        return Response({}, status=status.HTTP_200_OK)

