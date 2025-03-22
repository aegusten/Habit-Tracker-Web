from django.db import models
from django.conf import settings

class Habit(models.Model):
    TIMELINE_CHOICES = [
        ('1', '1 Month'),
        ('2', '2 Months'),
    ]
    REMINDER_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]
    INSIGHTS_CHOICES = [
        ('graph', 'Graph'),
        ('chart', 'Chart'),
        ('both', 'Both'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    timeline = models.CharField(max_length=1, choices=TIMELINE_CHOICES)
    motivational_reminder = models.CharField(max_length=6, choices=REMINDER_CHOICES)
    insights_method = models.CharField(max_length=5, choices=INSIGHTS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    
    metrics = models.JSONField(default=dict)   
    targets = models.JSONField(default=dict) 

    def __str__(self):
        return self.name

class HabitRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    data = models.JSONField()                

    class Meta:
        unique_together = ('habit','date')