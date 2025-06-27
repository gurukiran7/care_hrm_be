from care.emr.api.viewsets.base import EMRModelViewSet
from hrm.models.leave_type import LeaveType
from hrm.resources.leave_type import (
    LeaveTypeCreateSpec,
    LeaveTypeUpdateSpec,
    LeaveTypeRetrieveSpec,
    LeaveTypeListSpec,
)

class LeaveTypeViewSet(EMRModelViewSet):
    database_model = LeaveType
    pydantic_model = LeaveTypeCreateSpec
    pydantic_update_model = LeaveTypeUpdateSpec
    pydantic_read_model = LeaveTypeListSpec
    pydantic_retrieve_model = LeaveTypeRetrieveSpec
    