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
      return super().get_queryset().filter(
        file_type="employee",
        file_category="employee_document"
    )