# Generated by Django 3.2.25 on 2025-04-02 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('habits', '0006_delete_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='HabitBadge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge_type', models.CharField(choices=[('silver', 'Silver'), ('gold', 'Gold'), ('platinum', 'Platinum'), ('streak_10', 'Streak 10'), ('completed_preset', 'Completed Preset')], max_length=50)),
                ('active', models.BooleanField(default=False)),
                ('achieved_date', models.DateField(blank=True, null=True)),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habit_badges', to='habits.habit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habit_badges', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
