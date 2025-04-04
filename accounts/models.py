from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager
from django.conf import settings
from django.utils.timezone import now

class User(AbstractBaseUser, PermissionsMixin):
    id_number = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    login_count = models.PositiveIntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'id_number'
    REQUIRED_FIELDS = ['phone_number', 'age', 'full_name']

    def __str__(self):
        return self.id_number
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notifications_enabled = models.BooleanField(default=True)
    notification_frequency = models.CharField(max_length=10, choices=[('daily', 'Daily'), ('weekly', 'Weekly')], default='daily')


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
    
class UserAchievement(models.Model):
    BADGE_CHOICES = [
        ('login_streak_badge', 'Login Streak'),
        ('consistency_badge', 'Consistency'),
        ('first_win_badge', 'First Win'),
        ('triple_habit_badge', 'Triple Habit'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    badge_type = models.CharField(max_length=50, choices=BADGE_CHOICES)
    is_active = models.BooleanField(default=True)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge_type')

    def __str__(self):
        return f"{self.user.id_number} - {self.badge_type}"