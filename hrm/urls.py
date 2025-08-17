from rest_framework.routers import DefaultRouter

from hrm.api.viewsets.hrm import HelloViewset
from hrm.api.viewsets.employee_profile import EmployeeProfileViewSet
from hrm.api.viewsets.leave_request import LeaveRequestViewSet
from hrm.api.viewsets.leave_balance import LeaveBalanceViewSet
from hrm.api.viewsets.leave_type import LeaveTypeViewSet
from hrm.api.viewsets.employee_document import EmployeeDocumentViewSet
router = DefaultRouter()

router.register("hello", HelloViewset, basename="hrm-hello")
router.register("employees", EmployeeProfileViewSet, basename="hrm-employees")
router.register("leaves", LeaveRequestViewSet, basename="hrm-leaves")
router.register("leave-balances", LeaveBalanceViewSet, basename="hrm-leave-balances")
router.register("leave-types", LeaveTypeViewSet, basename="hrm-leave-types")
router.register('employee-documents', EmployeeDocumentViewSet, basename='employee-document')

urlpatterns = router.urls
