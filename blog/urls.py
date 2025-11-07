from django.urls import path
from rest_framework.routers import DefaultRouter

from blog.views import PostViewSet, BlogsFeedViewSet

router = DefaultRouter()

router.register("posts", PostViewSet, basename="posts")

urlpatterns = [
    path("feed/", BlogsFeedViewSet.as_view({"get": "list"}), name="feed"),
]

urlpatterns += router.urls
