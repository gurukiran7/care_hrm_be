from care.emr.resources.base import EMRResource
from pydantic import UUID4, Field
from typing import Optional
from hrm.models.holiday import Holiday

class HolidayBaseSpec(EMRResource):
    __model__ = Holiday

    id: Optional[UUID4] = None
    name: str = Field(max_length=100)
    date: str
    description: Optional[str] = None

class HolidayCreateSpec(HolidayBaseSpec):
    pass

class HolidayUpdateSpec(HolidayBaseSpec):
    name: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None

class HolidayRetrieveSpec(HolidayBaseSpec):
    pass

class HolidayListSpec(HolidayRetrieveSpec):
    pass