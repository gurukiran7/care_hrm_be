from care.emr.api.viewsets.base import (
    EMRCreateMixin,
    EMRRetrieveMixin,
    EMRUpdateMixin,
    EMRListMixin,
    EMRBaseViewSet,
)
from care.emr.models import FileUpload
from hrm.resources.employee_document import EmployeeDocumentUploadSpec
from care.emr.resources.file_upload.spec import (
    FileUploadRetrieveSpec,
    FileUploadListSpec,
    FileUploadUpdateSpec,
)
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


class EmployeeDocumentFilter(filters.FilterSet):
    is_archived = filters.BooleanFilter(field_name="is_archived")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")


class EmployeeDocumentViewSet(
    EMRCreateMixin,
    EMRRetrieveMixin,
    EMRUpdateMixin,
    EMRListMixin,
    EMRBaseViewSet,
):
    lookup_field = "external_id"
    database_model = FileUpload
    pydantic_model = EmployeeDocumentUploadSpec
    pydantic_read_model = FileUploadRetrieveSpec
    pydantic_update_model = FileUploadUpdateSpec
    pydantic_list_model = FileUploadListSpec
    filterset_class = EmployeeDocumentFilter
    filter_backends = [filters.DjangoFilterBackend]

    def get_queryset(self):
        return super().get_queryset().filter(
            file_type="employee",
            file_category="employee_document"
        )

    @action(detail=True, methods=["POST"], url_path="mark_upload_completed")
    def mark_upload_completed(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.upload_completed = True
        obj.save(update_fields=["upload_completed"])
        return Response(FileUploadRetrieveSpec.serialize(obj).to_json())