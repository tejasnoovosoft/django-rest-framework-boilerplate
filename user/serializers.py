from rest_framework import serializers

from user.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "contact_number", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class UserBasicDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "id")


class UserDetailsSerializer(serializers.ModelSerializer):
    followers = serializers.IntegerField(source="followers_count", read_only=True)
    following = serializers.IntegerField(source="following_count", read_only=True)

    class Meta:
        model = User
        exclude = ("password", "user_permissions", "groups")
