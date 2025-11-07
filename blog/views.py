from django.db.models import Count, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from blog.models import Post
from blog.serializers import PostWriteSerializer, PostReadSerializer
from social.models import Comment
from user.enums import UserRole


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["category"]

    search_fields = ["title", "content", "category__name"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PostWriteSerializer
        return PostReadSerializer

    def get_queryset(self):
        queryset = (
            Post.objects.select_related("author", "category")
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


class BlogsFeedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostReadSerializer

    def get_queryset(self):
        following_user_ids = self.request.user.following.values_list(
            "following_id", flat=True
        )

        return (
            Post.objects.filter(author_id__in=following_user_ids)
            .select_related("author", "category")
            .prefetch_related("comments")
            .order_by("-created_at")
            .annotate(likes_count=Count("likes", distinct=True))
        )
