from care.emr.api.viewsets.base import EMRModelViewSet
from hrm.models.leave_balance import LeaveBalance
from hrm.resources.leave_balance import (
    LeaveBalanceCreateSpec,
    LeaveBalanceUpdateSpec,
    LeaveBalanceRetrieveSpec,
    LeaveBalanceListSpec,
)
from django_filters import rest_framework as filters
from care.security.authorization import AuthorizationController
from rest_framework.exceptions import PermissionDenied

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

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(leave_type__deleted=False)


    def authorize_update(self, request_obj, model_instance):
        if not AuthorizationController.call(
            "can_update_leave_balance", self.request.user, model_instance
        ):
            raise PermissionDenied("You do not have permission to update leave balances.")

    def authorize_list(self, request_obj):
        if not AuthorizationController.call(
            "can_list_leave_balances", self.request.user
        ):
            raise PermissionDenied("You do not have permission to list leave balances.")
