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
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from pydantic import BaseModel


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
    database_model = FileUpload
    pydantic_model = EmployeeDocumentUploadSpec
    pydantic_read_model = FileUploadRetrieveSpec
    pydantic_update_model = FileUploadUpdateSpec
    pydantic_list_model = FileUploadListSpec
    filterset_class = EmployeeDocumentFilter
    filter_backends = [filters.DjangoFilterBackend]

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            file_type="employee",
            file_category="employee_document"
        )
        associating_id = self.request.query_params.get("associating_id")
        if associating_id:
            queryset = queryset.filter(associating_id=associating_id)
        return queryset

    @action(detail=True, methods=["POST"], url_path="mark_upload_completed")
    def mark_upload_completed(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.upload_completed = True
        obj.save(update_fields=["upload_completed"])
        return Response(FileUploadRetrieveSpec.serialize(obj).to_json())

    class ArchiveRequestSpec(BaseModel):
        archive_reason: str

    @action(detail=True, methods=["POST"], url_path="archive")
    def archive(self, request, *args, **kwargs):
        obj = self.get_object()
        request_data = self.ArchiveRequestSpec(**request.data)
        obj.is_archived = True
        obj.archive_reason = request_data.archive_reason
        obj.archived_datetime = timezone.now()
        obj.archived_by = request.user
        obj.save(
            update_fields=[
                "is_archived",
                "archive_reason",
                "archived_datetime",
                "archived_by",
            ]
        )
        return Response(FileUploadRetrieveSpec.serialize(obj).to_json())