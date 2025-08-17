from care.emr.api.viewsets.base import EMRModelViewSet
from hrm.models.leave_balance import LeaveBalance
from hrm.resources.leave_balance import (
    LeaveBalanceCreateSpec,
    LeaveBalanceUpdateSpec,
    LeaveBalanceRetrieveSpec,
    LeaveBalanceListSpec,
)
from django_filters import rest_framework as filters

class LeaveBalanceFilters(filters.FilterSet):
    employee = filters.UUIDFilter(field_name="employee__external_id")
    leave_type = filters.UUIDFilter(field_name="leave_type__external_id")

    class Meta:
        model = LeaveBalance
        fields = ["employee", "leave_type"]

class LeaveBalanceViewSet(EMRModelViewSet):
    database_model = LeaveBalance
    pydantic_model = LeaveBalanceCreateSpec
    pydantic_update_model = LeaveBalanceUpdateSpec
    pydantic_read_model = LeaveBalanceListSpec
    pydantic_retrieve_model = LeaveBalanceRetrieveSpec
    filterset_class = LeaveBalanceFilters
    filter_backends = [filters.DjangoFilterBackend]


    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
