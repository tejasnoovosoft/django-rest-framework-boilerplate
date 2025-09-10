from rest_framework.routers import DefaultRouter

from blog.views import PostViewSet

router = DefaultRouter()

router.register('posts', PostViewSet, basename='posts')

urlpatterns = router.urls
