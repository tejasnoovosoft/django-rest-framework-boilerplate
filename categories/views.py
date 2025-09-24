from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from categories.models import Category
from categories.serializers import CategorySerializer
from core.permissions import IsAdmin


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]
