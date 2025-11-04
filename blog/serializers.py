from rest_framework import serializers

from blog.models import Post
from categories.serializers import CategorySerializer
from social.serializers import CommentSerializer
from user.serializers import UserSerializer


class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content", "category", "created_at"]
        read_only_fields = ["created_at"]


class PostReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_comments(self, post):
        comments = post.comments.all()
        return CommentSerializer(comments, many=True).data
