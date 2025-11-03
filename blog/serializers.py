from rest_framework import serializers

from blog.models import Post
from social.serializers import CommentSerializer
from user.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author', 'created_at']

    def get_comments(self, post):
        comments = post.comment_set.all()
        return CommentSerializer(comments, many=True).data
