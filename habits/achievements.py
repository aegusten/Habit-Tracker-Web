from django.utils.timezone import now
from habits.models import Habit, HabitRecord, HabitAchievement
from accounts.models import UserAchievement

def award_user_badge(user, badge_type, condition):
    if condition:
        UserAchievement.objects.update_or_create(
            user=user,
            badge_type=badge_type,
            defaults={'is_active': True, 'awarded_at': now()}
        )
    else:
        UserAchievement.objects.filter(user=user, badge_type=badge_type).update(is_active=False)

def award_habit_badge(user, habit, badge_type, condition):
    if condition:
        HabitAchievement.objects.update_or_create(
            user=user,
            habit=habit,
            badge_type=badge_type,
            defaults={'is_active': True, 'awarded_at': now()}
        )
    else:
        HabitAchievement.objects.filter(user=user, habit=habit, badge_type=badge_type).update(is_active=False)

def compute_user_achievements(user):
    badges = {
        'login_streak_badge': False,
        'consistency_badge': False,
        'first_win_badge': False,
        'triple_habit_badge': False,
    }

    if user.login_count >= 10:
        badges['login_streak_badge'] = True
        award_user_badge(user, 'login_streak_badge', True)
    else:
        award_user_badge(user, 'login_streak_badge', False)

    unique_log_days = HabitRecord.objects.filter(habit__user=user).values('date').distinct().count()
    if unique_log_days >= 20:
        badges['consistency_badge'] = True
        award_user_badge(user, 'consistency_badge', True)
    else:
        award_user_badge(user, 'consistency_badge', False)

    if Habit.objects.filter(user=user, achieved=True).exists():
        badges['first_win_badge'] = True
        award_user_badge(user, 'first_win_badge', True)
    else:
        award_user_badge(user, 'first_win_badge', False)

    preset_completed = Habit.objects.filter(user=user, achieved=True, template_key__isnull=False).count()
    if preset_completed >= 3:
        badges['triple_habit_badge'] = True
        award_user_badge(user, 'triple_habit_badge', True)
    else:
        award_user_badge(user, 'triple_habit_badge', False)

    return badges


def compute_habit_achievements(habit):
    user = habit.user
    points = habit.points
    achievements = {}

    silver = points > 0 and points < 75
    gold = points >= 75 and points < 150
    platinum = points >= 150
    streak_10 = habit.streak >= 10
    completed = habit.template_key is not None and habit.achieved

    award_habit_badge(user, habit, 'silver_badge', silver)
    award_habit_badge(user, habit, 'gold_badge', gold)
    award_habit_badge(user, habit, 'platinum_badge', platinum)
    award_habit_badge(user, habit, 'streak_10_badge', streak_10)
    award_habit_badge(user, habit, 'completed_preset_badge', completed)

    achievements['silver_badge'] = silver
    achievements['gold_badge'] = gold
    achievements['platinum_badge'] = platinum
    achievements['streak_10_badge'] = streak_10 
    achievements['completed_preset_badge'] = completed

    return achievements

