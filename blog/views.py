from rest_framework import viewsets, request
from rest_framework.permissions import IsAuthenticated

from blog.models import Post
from blog.serializers import PostSerializer
from user.enums import UserRole


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = PostSerializer

    def get_queryset(self):
        if self.request.user.role == UserRole.ADMIN.value:
            return Post.objects.select_related('author').all()
        else:
            return Post.objects.select_related('author').filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
