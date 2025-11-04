from django.urls import path

from social.views import ToggleLikeAPIView, CommentViewSet, ToggleFollowAPIView

urlpatterns = [
    path("posts/<int:post_id>/toggle-like/", ToggleLikeAPIView.as_view()),
    path("posts/<int:post_id>/comment/", CommentViewSet.as_view({"post": "create"})),
    path("users/<int:user_id>/toggle-follow/", ToggleFollowAPIView.as_view()),
]
