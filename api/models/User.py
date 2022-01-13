from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=500, unique=True)
    password = models.CharField(max_length=255)
    namespace = models.CharField(max_length=63, unique=True)
    role = models.CharField(max_length=255, default="user")
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
