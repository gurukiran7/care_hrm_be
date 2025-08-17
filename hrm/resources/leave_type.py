# plugin/hrm/resources/leave/spec.py

from care.emr.resources.base import EMRResource
from pydantic import UUID4, Field
from typing import Optional
from hrm.models.leave_type import LeaveType

class LeaveTypeBaseSpec(EMRResource):
    __model__ = LeaveType

    id: Optional[UUID4] = None
    name: str = Field(max_length=100)
    default_days: int = 0

class LeaveTypeCreateSpec(LeaveTypeBaseSpec):
    pass

class LeaveTypeUpdateSpec(LeaveTypeBaseSpec):
    name: Optional[str] = None
    default_days: Optional[int] = None


class LeaveTypeRetrieveSpec(LeaveTypeBaseSpec):
    pass

class LeaveTypeListSpec(LeaveTypeRetrieveSpec):
    pass