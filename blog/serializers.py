from rest_framework import serializers

from blog.models import Post
from social.models import Like
from user.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author', 'created_at']

    def get_likes_count(self, post):
        return Like.objects.filter(post=post).count()
