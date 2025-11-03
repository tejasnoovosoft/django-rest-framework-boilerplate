from django.urls import path

from social.views import ToggleLikeAPIView, CommentViewSet

urlpatterns = [
    path("<int:post_id>/toggle-like/", ToggleLikeAPIView.as_view()),
    path("<int:post_id>/comment/", CommentViewSet.as_view({"post": "create"})),
]
