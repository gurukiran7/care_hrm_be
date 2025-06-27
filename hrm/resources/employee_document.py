from django.conf import settings
from django.core.exceptions import ValidationError
from pydantic import field_validator, BaseModel, UUID4
from care.emr.resources.base import EMRResource
from care.utils.models.validators import file_name_validator
from care.emr.resources.file_upload.spec import FileUploadBaseSpec

class EmployeeDocumentUploadSpec(FileUploadBaseSpec):
    original_name: str
    file_type: str = "employee"
    file_category: str = "employee_document"
    associating_id: UUID4
    mime_type: str

    def perform_extra_deserialization(self, is_update, obj):
        # Authz Performed in the request
        obj._just_created = True  # noqa SLF001
        obj.internal_name = self.original_name
        obj.meta["mime_type"] = self.mime_type

    @field_validator("mime_type")
    @classmethod 
    def validate_mime_type(cls, mime_type: str):
        if mime_type not in settings.ALLOWED_MIME_TYPES:
            raise ValueError("Invalid mime type")
        return mime_type

    
    @field_validator("original_name")
    @classmethod
    def validate_original_name(cls, original_name: str):
        if not original_name:
            raise ValueError("File name cannot be empty")
        try:
            file_name_validator(original_name)
        except ValidationError as e:
            raise ValueError(e.message) from e 
        return original_name

