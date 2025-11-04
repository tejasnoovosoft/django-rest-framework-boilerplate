from rest_framework import status, viewsets, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Post
from social.models import Like, Comment, Follow
from social.serializers import CommentSerializer
from user.models import User


# Create your views here.
class ToggleLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        user = request.user

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        like, created = Like.objects.get_or_create(post=post, user=user)

        if not created:
            like.delete()
            return Response({"message": "Post unliked"}, status=status.HTTP_200_OK)

        return Response({"message": "Post liked"}, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(post_id=post_id).order_by("-created_at")

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError({"post": "Post not found."})

        serializer.save(user=self.request.user, post=post)


class ToggleFollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        follower = request.user

        # Prevent self-following
        if follower.id == user_id:
            return Response(
                {"message": "You can't follow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # The user you want to follow/unfollow
        following = get_object_or_404(User, id=user_id)

        # Try to delete existing follow relation (one db call)
        deleted, _ = Follow.objects.filter(
            follower=follower, following=following
        ).delete()

        if deleted:
            return Response(
                {"message": f"Unfollowed {following.first_name} {following.last_name}"},
                status=status.HTTP_200_OK,
            )

        # Otherwise create the follow relation
        Follow.objects.create(follower=follower, following=following)

        return Response(
            {"message": f"Following {following.first_name} {following.last_name}"},
            status=status.HTTP_201_CREATED,
        )
