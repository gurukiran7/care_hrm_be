from care.emr.api.viewsets.base import EMRModelViewSet
from hrm.models.leave_type import LeaveType
from hrm.resources.leave_type import (
    LeaveTypeCreateSpec,
    LeaveTypeUpdateSpec,
    LeaveTypeRetrieveSpec,
    LeaveTypeListSpec,
)
from care.security.authorization import AuthorizationController
from rest_framework.exceptions import PermissionDenied

from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

class LeaveTypeViewSet(EMRModelViewSet):
    database_model = LeaveType
    pydantic_model = LeaveTypeCreateSpec
    pydantic_update_model = LeaveTypeUpdateSpec
    pydantic_read_model = LeaveTypeListSpec
    pydantic_retrieve_model = LeaveTypeRetrieveSpec

    def authorize_create(self, request_obj):
        if not AuthorizationController.call(
            "can_create_leave_type", self.request.user
        ):
            raise PermissionDenied("You do not have permission to create leave types.")

    def authorize_update(self, request_obj, model_instance):
        if not AuthorizationController.call(
            "can_update_leave_type", self.request.user, model_instance
        ):
            raise PermissionDenied("You do not have permission to update leave types.")

    def authorize_destroy(self, instance):
        if not AuthorizationController.call(
            "can_delete_leave_type", self.request.user, instance
        ):
            raise PermissionDenied("You do not have permission to delete leave types.")

    def authorize_list(self, request_obj):
        if not AuthorizationController.call(
            "can_list_leave_types", self.request.user
        ):
            raise PermissionDenied("You do not have permission to list leave types.")
