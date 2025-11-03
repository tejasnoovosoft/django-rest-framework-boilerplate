from rest_framework import routers

from categories.views import CategoryViewSet

router = routers.DefaultRouter()
router.register("", CategoryViewSet)

urlpatterns = router.urls
