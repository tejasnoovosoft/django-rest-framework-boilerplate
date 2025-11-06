from django.db.models import Count
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserDetailsReadSerializer,
    UserDetailsWriteSerializer,
)
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class LoginView(APIView):
    """
    API endpoint for user login.
    Validates credentials and returns an auth token.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"detail": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "user_id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            status=status.HTTP_201_CREATED,
        )


class UserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)

        if self.request.method == "GET":
            queryset = queryset.annotate(
                followers_count=Count("followers", distinct=True),
                following_count=Count("following", distinct=True),
            )
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserDetailsReadSerializer
        return UserDetailsWriteSerializer

    def get_object(self):
        return self.get_queryset().get(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        if request.method == "PUT":
            raise MethodNotAllowed("PUT")
        return super().update(request, *args, **kwargs)
