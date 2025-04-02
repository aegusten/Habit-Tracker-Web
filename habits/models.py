from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.apps import apps

class Habit(models.Model):
    TIMELINE_CHOICES = [('1', '1 Month'), ('2', '2 Months')]
    REMINDER_CHOICES = [('daily', 'Daily'), ('weekly', 'Weekly')]
    INSIGHTS_CHOICES = [('graph', 'Graph'), ('chart', 'Chart'), ('both', 'Both')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    timeline = models.CharField(max_length=1, choices=TIMELINE_CHOICES)
    motivational_reminder = models.CharField(max_length=6, choices=REMINDER_CHOICES)
    insights_method = models.CharField(max_length=5, choices=INSIGHTS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    template_key = models.CharField(max_length=50, blank=True, null=True)


    metrics = models.JSONField(default=dict)

    targets = models.JSONField(default=dict) #remove
    achieved = models.BooleanField(default=False)
    achieved_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    def check_stop_smoking_progress(self):
        HabitRecord = apps.get_model('habits', 'HabitRecord')
        if 'cigarettes_per_day' not in self.metrics:
            return
        records = HabitRecord.objects.filter(habit=self).order_by('-date')
        required_streak = 5
        streak_count = 0
        for r in records:
            cigs = r.data.get('cigarettes_per_day')
            if str(cigs) in ['0', '0.0']:
                streak_count += 1
            else:
                break
        if streak_count >= required_streak and not self.achieved:
            self.achieved = True
            self.achieved_date = now().date()
            self.save()

    def check_wake_up_early_progress(self):
        HabitRecord = apps.get_model('habits', 'HabitRecord')
        if 'desired_wake_time' not in self.metrics:
            return
        desired_wake = self.metrics.get('desired_wake_time', {}).get('default', None)
        if not desired_wake:
            return
        records = HabitRecord.objects.filter(habit=self).order_by('-date')
        streak_needed = 5
        streak_count = 0
        for r in records:
            current_wake = r.data.get('current_wake_time')
            if current_wake and current_wake <= desired_wake:
                streak_count += 1
            else:
                break
        if streak_count >= streak_needed and not self.achieved:
            self.achieved = True
            self.achieved_date = now().date()
            self.save()

    def check_eat_healthy_progress(self):
        HabitRecord = apps.get_model('habits', 'HabitRecord')
        if 'fruit_veg_target' not in self.metrics:
            return
        target = int(self.metrics['fruit_veg_target'].get('default', 5))
        records = HabitRecord.objects.filter(habit=self).order_by('-date')
        success_streak_needed = 5
        success_streak = 0
        for r in records:
            daily_val = r.data.get('fruit_veg_target')
            if daily_val and int(daily_val) >= target:
                success_streak += 1
            else:
                break
        if success_streak >= success_streak_needed and not self.achieved:
            self.achieved = True
            self.achieved_date = now().date()
            self.save()


class HabitRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    data = models.JSONField()

    def __str__(self):
        return f"{self.habit.name} on {self.date}"

class HabitAchievement(models.Model):
    BADGE_CHOICES = [
        ('silver_badge', 'Silver'),
        ('gold_badge', 'Gold'),
        ('platinum_badge', 'Platinum'),
        ('streak_10_badge', '10-Day Streak'),
        ('completed_preset_badge', 'Completed Preset'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    habit = models.ForeignKey('Habit', on_delete=models.CASCADE)
    badge_type = models.CharField(max_length=50, choices=BADGE_CHOICES)
    is_active = models.BooleanField(default=True)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'habit', 'badge_type')

    def __str__(self):
        return f"{self.user} - {self.habit} - {self.badge_type}"