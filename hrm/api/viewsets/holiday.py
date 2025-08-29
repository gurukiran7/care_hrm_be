from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from care.emr.api.viewsets.base import (
    EMRBaseViewSet, EMRCreateMixin, EMRListMixin, EMRRetrieveMixin, EMRUpdateMixin
)
from hrm.models.holiday import Holiday
from hrm.resources.holiday import (
    HolidayCreateSpec, HolidayUpdateSpec, HolidayRetrieveSpec, HolidayListSpec
)
from care.security.authorization import AuthorizationController
from rest_framework.exceptions import PermissionDenied

class HolidayFilters(filters.FilterSet):
    date = filters.DateFilter(field_name="date")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    date__gte = filters.DateFilter(field_name="date", lookup_expr="gte")
    date__lte = filters.DateFilter(field_name="date", lookup_expr="lte")

class HolidayViewSet(EMRCreateMixin, EMRRetrieveMixin, EMRUpdateMixin, EMRListMixin, EMRBaseViewSet):
    database_model = Holiday
    pydantic_model = HolidayCreateSpec
    pydantic_update_model = HolidayUpdateSpec
    pydantic_read_model = HolidayListSpec
    pydantic_retrieve_model = HolidayRetrieveSpec
    filterset_class = HolidayFilters
    filter_backends = [filters.DjangoFilterBackend]

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


    def authorize_create(self, request_obj):
        if not AuthorizationController.call(
            "can_create_holiday", self.request.user
        ):
            raise PermissionDenied("You do not have permission to create holidays.")

    def authorize_update(self, request_obj, model_instance):
        if not AuthorizationController.call(
            "can_update_holiday", self.request.user, model_instance
        ):
            raise PermissionDenied("You do not have permission to update holidays.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def authorize_destroy(self, instance):
        if not AuthorizationController.call(
            "can_delete_holiday", self.request.user, instance
        ):
            raise PermissionDenied("You do not have permission to delete holidays.")

    def authorize_list(self, request_obj):
        if not AuthorizationController.call(
            "can_list_holidays", self.request.user
        ):
            raise PermissionDenied("You do not have permission to list holidays.")