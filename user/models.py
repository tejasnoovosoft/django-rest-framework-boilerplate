from django.contrib.auth.models import AbstractUser
from django.db import models

from user.enums import UserRole
from user.managers import UserManager


class User(AbstractUser):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(max_length=254, unique=True)
    contact_number = models.CharField(max_length=10, null=True, blank=True)
    password = models.CharField()
    username = None
    role = models.CharField(
        max_length=10, choices=UserRole.choices(), default=UserRole.USER.value
    )
    bio = models.TextField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
