from rest_framework import serializers

from user.models import User
from utils.cloudinary_utils import upload_profile_picture


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "contact_number",
            "password",
            "profile_picture",
        )

    def create(self, validated_data):
        profile_picture = validated_data.pop("profile_picture", None)

        profile_picture_url = upload_profile_picture(profile_picture)

        user = User.objects.create_user(
            **validated_data, profile_picture=profile_picture_url
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class UserBasicDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "id", "bio")


class UserDetailsReadSerializer(serializers.ModelSerializer):
    followers = serializers.IntegerField(source="followers_count", read_only=True)
    following = serializers.IntegerField(source="following_count", read_only=True)

    class Meta:
        model = User
        exclude = ("password", "user_permissions", "groups")


class UserDetailsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "bio")
