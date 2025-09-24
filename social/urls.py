from django.urls import path

from social.views import ToggleLikeAPIView

urlpatterns = [
    path('<int:post_id>/toggle-like/', ToggleLikeAPIView.as_view()),
]
