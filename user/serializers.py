import cloudinary.uploader
from rest_framework import serializers

from user.models import User


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

        # Create user without profile picture first
        user = User.objects.create_user(**validated_data)

        # Upload to Cloudinary if profile picture provided
        if profile_picture:
            upload_result = cloudinary.uploader.upload(
                profile_picture,
                folder="profile_pictures",
                public_id=f"user_{user.id}",
                overwrite=True,
                resource_type="image",
            )
            user.profile_picture = upload_result["secure_url"]
            user.save()

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
