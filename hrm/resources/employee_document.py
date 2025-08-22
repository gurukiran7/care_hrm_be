from enum import Enum
from pydantic import BaseModel, UUID4, field_validator
from django.conf import settings
from django.core.exceptions import ValidationError
from care.emr.resources.file_upload.spec import FileUploadBaseSpec
from care.utils.models.validators import file_name_validator

class EmployeeFileTypeChoices(str, Enum):
    employee = "employee"

class EmployeeFileCategoryChoices(str, Enum):
    employee_document = "employee_document"

class EmployeeDocumentUploadSpec(FileUploadBaseSpec):
    original_name: str
    file_type: EmployeeFileTypeChoices = EmployeeFileTypeChoices.employee
    file_category: EmployeeFileCategoryChoices = EmployeeFileCategoryChoices.employee_document
    associating_id: UUID4
    mime_type: str

    def perform_extra_deserialization(self, is_update, obj):
        obj._just_created = True  # noqa SLF001
        obj.internal_name = self.original_name
        obj.meta["mime_type"] = self.mime_type
        obj.file_type = self.file_type or "employee"
        obj.file_category = self.file_category or "employee_document"

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

