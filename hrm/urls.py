from rest_framework.routers import DefaultRouter

from hrm.api.viewsets.hrm import HelloViewset

from hrm.api.viewsets.employee_profile import EmployeeProfileViewSet
from hrm.api.viewsets.leave_request import LeaveRequestViewSet

router = DefaultRouter()

router.register("hello", HelloViewset, basename="hrm-hello")
router.register("hrm/employees", EmployeeProfileViewSet, basename="hrm-employees")
router.register("hrm/leaves", LeaveRequestViewSet, basename="hrm-leaves")

urlpatterns = router.urls
