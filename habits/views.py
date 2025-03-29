from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode

from django.utils import timezone
from .forms import HabitForm
from .models import Habit, HabitRecord
from django.http import JsonResponse

from .utils import (
    PRESET_HABITS,
    PRESET_TEMPLATES,
    AWARD_MESSAGES,
    NOTIFICATION_MESSAGES
)



@login_required
def form_new_habit_view(request):

    template_key = request.GET.get('template')
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.template_key = template_key

            if template_key in PRESET_HABITS:
                preset = PRESET_HABITS[template_key]
                metric_data = {}
                for field in preset.get('extra_fields', []):
                    key = field['key']
                    val = request.POST.get(key, '')

                    if template_key == 'stop_smoking':
                        if key in ['cigarettes_per_day', 'craving_level']:
                            importance = 'daily_required'
                        else:
                            importance = 'static_display'
                    elif template_key == 'wake_up_early':
                        importance = 'daily_required'
                    elif template_key == 'eat_healthy':
                        importance = 'daily_required'
                    else:
                        importance = 'static_display'

                    metric_data[key] = {
                        'type': field['type'],
                        'label': field['label'],
                        'default': val,
                        'importance': importance
                    }
                habit.metrics = metric_data

            custom_keys = request.POST.getlist('custom_field_key[]', [])
            custom_types = request.POST.getlist('custom_field_type[]', [])
            custom_values = request.POST.getlist('custom_field_value[]', [])
            custom_importances = request.POST.getlist('custom_field_required[]', [])

            for i in range(len(custom_keys)):
                field_name = custom_keys[i].strip()
                field_type = custom_types[i].strip() if i < len(custom_types) else ''
                default_val = custom_values[i].strip() if i < len(custom_values) else ''
                old_importance = custom_importances[i] if i < len(custom_importances) else 'optional'

                if old_importance == 'relevant':
                    importance = 'daily_required'
                elif old_importance == 'optional':
                    importance = 'daily_optional'
                elif old_importance == 'display':
                    importance = 'static_display'
                else:
                    importance = 'daily_optional'

                if field_name:
                    habit.metrics[field_name] = {
                        'type': field_type,
                        'label': field_name.title(),
                        'default': default_val,
                        'importance': importance
                    }

            habit.save()
            return redirect('habits:ongoing_habit')
    else:
        form = HabitForm()

    return render(request, 'form_new_habit.html', {
        'form': form,
        'templates': PRESET_TEMPLATES,
        'template': template_key
    })

@login_required
def ongoing_habit_view(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'ongoing_habit.html', {'habits': habits})

@login_required
def insert_data_view(request, habit_id):
    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)
    records = HabitRecord.objects.filter(habit=habit).order_by('-date')
    if records.exists():
        next_date = records.first().date + timezone.timedelta(days=1)
    else:
        next_date = timezone.now().date()

    preset_fields = []
    custom_fields = []
    static_display_fields = []

    PRESET_KEYS = [
        'cigarettes_per_day', 'craving_level', 'planned_quit_date', 'nicotine_replacement',
        'trigger_coping', 'current_wake_time', 'desired_wake_time', 'bedtime', 'sleep_quality',
        'snooze_count', 'daily_calorie_target', 'fruit_veg_target', 'water_intake_goal',
        'junk_food_consumption'
    ]

    for field_name, info in habit.metrics.items():
        imp = info.get('importance', 'daily_optional')
        if imp == 'static_display':
            static_display_fields.append((field_name, info))
        elif imp in ['daily_required', 'daily_optional']:
            if field_name in PRESET_KEYS:
                preset_fields.append((field_name, info))
            else:
                custom_fields.append((field_name, info))

    if request.method == "POST":
        data = {}
        for field_name, info in preset_fields + custom_fields:
            posted_val = request.POST.get(field_name, '')
            if info.get('importance') == 'daily_required' and not posted_val:
                posted_val = "MISSING"
            data[field_name] = posted_val

        HabitRecord.objects.create(
            habit=habit,
            date=next_date,
            data=data
        )

        if habit.template_key == 'stop_smoking':
            habit.check_stop_smoking_progress()
        elif habit.template_key == 'wake_up_early':
            habit.check_wake_up_early_progress()
        elif habit.template_key == 'eat_healthy':
            habit.check_eat_healthy_progress()

        habit.streak += 1
        habit.points += 1
        habit.save()

        message_index = min(habit.streak - 1, 4)
        habit_type = habit.template_key or 'custom'
        message = AWARD_MESSAGES.get(habit_type, AWARD_MESSAGES['custom'])[message_index]

        query = urlencode({'success': 1, 'msg': message})
        return redirect(f"{request.path}?{query}")

    return render(request, 'track_habits/insert_data.html', {
        'habit': habit,
        'records': records,
        'next_date': next_date,
        'preset_fields': preset_fields,
        'custom_fields': custom_fields,
        'static_display_fields': static_display_fields
    })

@login_required
def track_habit_detail_view(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit_records = HabitRecord.objects.filter(habit=habit).order_by("date")

    numeric_fields = []
    for key, info in habit.metrics.items():
        if info.get('importance') in ['daily_required','daily_optional'] and info.get('type') == 'number':
            numeric_fields.append(key)

    chart_data = []
    for rec in habit_records:
        row = {'date': rec.date.strftime('%Y-%m-%d')}
        for nf in numeric_fields:
            val_str = rec.data.get(nf, '0')
            try:
                row[nf] = float(val_str)
            except ValueError:
                row[nf] = 0.0
        chart_data.append(row)

    streak = habit.streak
    total_points = habit.points
    badge = None
    if total_points >= 150:
        badge = "Platinum"
    elif total_points >= 75:
        badge = "Gold"
    elif total_points > 0:
        badge = "Silver"

    return render(request, 'track_habits/track_habit_detail.html', {
        "habit": habit,
        "habit_records": habit_records,
        "chart_data": chart_data,
        "numeric_fields": numeric_fields,
        "streak": streak,
        "total_points": total_points,
        "badge": badge
    })

@login_required
def abort_process_view(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.delete()
    return redirect('habits:ongoing_habit')

@login_required
def notification_dashboard_view(request):
    user = request.user
    habits = Habit.objects.filter(user=user)

    grouped = {}

    for habit in habits:
        key = habit.template_key or 'custom'
        if key not in grouped:
            grouped[key] = {
                'daily': [],
                'weekly': []
            }
        grouped[key][habit.motivational_reminder].append(habit)

    return render(request, 'notifications/dashboard.html', {
        'grouped_habits': grouped
    })

@csrf_exempt
@login_required
def push_notification(request):
    if request.method == "POST":
        habit_type = request.POST.get("habit_type")
        stage = int(request.POST.get("stage", 0))

        message_list = NOTIFICATION_MESSAGES.get(habit_type, NOTIFICATION_MESSAGES['custom'])
        message = message_list[stage] if stage < len(message_list) else message_list[-1]

        return JsonResponse({"message": message})

    return JsonResponse({"error": "Invalid request"}, status=400)