from rest_framework.routers import DefaultRouter

from hrm.api.viewsets.hrm import HelloViewset

router = DefaultRouter()

router.register("hrm", HelloViewset, basename="hrm__hrm")

urlpatterns = router.urls
