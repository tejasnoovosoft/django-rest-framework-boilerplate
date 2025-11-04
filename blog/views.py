from django.db.models import Count, Prefetch
from rest_framework import viewsets, request
from rest_framework.permissions import IsAuthenticated

from blog.models import Post
from blog.serializers import PostSerializer
from social.models import Comment
from user.enums import UserRole


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = PostSerializer

    def get_queryset(self):

        queryset = (
            Post.objects.select_related("author")
            .prefetch_related(
                Prefetch(
                    "comments",
                    queryset=Comment.objects.select_related("user").order_by(
                        "-created_at"
                    ),
                )
            )
            .annotate(likes_count=Count("likes", distinct=True))
        )

        if self.request.user.role == UserRole.ADMIN.value:
            return queryset.all()
        else:
            return queryset.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
