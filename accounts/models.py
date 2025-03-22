from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager
from django.conf import settings

class User(AbstractBaseUser, PermissionsMixin):
    id_number = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'id_number'
    REQUIRED_FIELDS = ['phone_number', 'age', 'full_name']

    def __str__(self):
        return self.id_number

class SecurityQuestion(models.Model):
    question_text = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text
    
class UserSecurityAnswer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='security_answers'
    )
    
    question = models.ForeignKey(SecurityQuestion, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255, default="") 
    answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.id_number} - {self.question.question_text}"