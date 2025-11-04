from rest_framework import serializers

from social.models import Comment, Follow
from user.serializers import UserBasicDetailsSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("user", "post")


class FollowingSerializer(serializers.ModelSerializer):
    following = UserBasicDetailsSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ["id", "following", "created_at"]


class FollowersSerializer(serializers.ModelSerializer):
    follower = UserBasicDetailsSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ["id", "follower", "created_at"]
