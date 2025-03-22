from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    id_number = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    pet_name = models.CharField(max_length=100, blank=True, null=True)
    first_love = models.CharField(max_length=100, blank=True, null=True)
    favorite_color = models.CharField(max_length=50, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'id_number'
    REQUIRED_FIELDS = ['phone_number', 'age', 'full_name']

    def __str__(self):
        return self.id_number
