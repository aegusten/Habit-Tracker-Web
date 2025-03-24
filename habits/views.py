from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import now
from .forms import HabitForm, HabitRecordForm
from .models import Habit, HabitRecord

PRESET_HABITS = {
    'stop_smoking': {
        'metrics': {
            'cigarettes_per_day': 0,
            'craving_level': None,
            'planned_quit_date': None,
            'nicotine_replacement': '',
            'trigger_coping': ''
        },
        'targets': {
            'cigarettes_per_day': 0
        },
        'extra_fields': [
            {'key': 'cigarettes_per_day', 'label': 'Cigarettes per Day', 'type': 'number'},
            {'key': 'craving_level', 'label': 'Craving Level (1-10)', 'type': 'number'},
            {'key': 'planned_quit_date', 'label': 'Planned Quit Date', 'type': 'date'},
            {'key': 'nicotine_replacement', 'label': 'Nicotine Replacement', 'type': 'text'},
            {'key': 'trigger_coping', 'label': 'Triggers & Coping Strategies', 'type': 'textarea'}
        ]
    },
    'wake_up_early': {
        'metrics': {
            'current_wake_time': None,
            'desired_wake_time': None,
            'bedtime': None,
            'sleep_quality': None,
            'snooze_count': 0
        },
        'targets': {},
        'extra_fields': [
            {'key': 'current_wake_time', 'label': 'Current Wake Time', 'type': 'time'},
            {'key': 'desired_wake_time', 'label': 'Desired Wake Time', 'type': 'time'},
            {'key': 'bedtime', 'label': 'Bedtime', 'type': 'time'},
            {'key': 'sleep_quality', 'label': 'Sleep Quality (1-10)', 'type': 'number'},
            {'key': 'snooze_count', 'label': 'Number of Snoozes', 'type': 'number'}
        ]
    },
    'eat_healthy': {
        'metrics': {
            'daily_calorie_target': 2000,
            'fruit_veg_target': 5,
            'water_intake_goal': 8,
            'junk_food_consumption': 0
        },
        'targets': {
            'fruit_veg_target': 5,
            'water_intake_goal': 8
        },
        'extra_fields': [
            {'key': 'daily_calorie_target', 'label': 'Daily Calorie Target', 'type': 'number'},
            {'key': 'fruit_veg_target', 'label': 'Fruit & Vegetable Servings', 'type': 'number'},
            {'key': 'water_intake_goal', 'label': 'Water Intake (glasses/day)', 'type': 'number'},
            {'key': 'junk_food_consumption', 'label': 'Junk Food Consumption', 'type': 'number'}
        ]
    }
}

PRESET_TEMPLATES = [
    {'key': 'stop_smoking', 'icon': 'bi-emoji-smile', 'label': 'Stop Smoking'},
    {'key': 'wake_up_early', 'icon': 'bi-sunrise', 'label': 'Wake Up Early'},
    {'key': 'eat_healthy', 'icon': 'bi-apple', 'label': 'Eat Healthy'},
    {'key': 'custom', 'icon': 'bi-pencil-square', 'label': 'Custom'}
]

@login_required
def form_new_habit_view(request):
    template_key = request.GET.get('template')
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            if template_key in PRESET_HABITS:
                preset = PRESET_HABITS[template_key]
                metric_data = {}
                for field in preset.get('extra_fields', []):
                    key = field['key']
                    val = request.POST.get(key, '')
                    metric_data[key] = {'type': field['type'], 'default': val}
                habit.metrics = metric_data
                habit.targets = preset.get('targets', {}).copy()
            custom_keys = request.POST.getlist('custom_field_key[]', [])
            custom_types = request.POST.getlist('custom_field_type[]', [])
            custom_values = request.POST.getlist('custom_field_value[]', [])
            for i in range(len(custom_keys)):
                field_name = custom_keys[i].strip()
                field_type = custom_types[i].strip()
                default_val = custom_values[i].strip()
                if field_name:
                    habit.metrics[field_name] = {'type': field_type, 'default': default_val}
            habit.save()
            return redirect('habits:ongoing_habit')
    else:
        form = HabitForm()
    return render(request, 'form_new_habit.html', {'form': form, 'templates': PRESET_TEMPLATES})

@login_required
def ongoing_habit_view(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'ongoing_habit.html', {'habits': habits})

@login_required
def abort_process_view(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.delete()
    return redirect('habits:ongoing_habit')

@login_required
def track_habit_detail_view(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    streak = habit.streak if habit.streak else 0
    total_points = habit.points
    badge = None
    if total_points >= 150:
        badge = "Platinum"
    elif total_points >= 75:
        badge = "Gold"
    elif total_points > 0:
        badge = "Silver"
    habit_records = HabitRecord.objects.filter(habit=habit).order_by("date")
    total_days = (habit.created_at.date() - now().date()).days
    days_remaining = habit.timeline
    committed_days = total_days - int(days_remaining) if total_days > 0 else 0
    if request.method == "POST":
        if "reminder_frequency" in request.POST:
            habit.motivational_reminder = request.POST["reminder_frequency"]
        if "timeline" in request.POST:
            habit.timeline = request.POST["timeline"]
        habit.save()
        return redirect('habits:track_habit_detail', habit_id=habit.id)
    return render(request, 'track_habits/track_habit_detail.html', {
        "habit": habit,
        "streak": streak,
        "total_points": total_points,
        "badge": badge,
        "habit_records": habit_records,
        "committed_days": committed_days,
        "days_remaining": days_remaining
    })

@login_required
def insert_data_view(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    today = timezone.now().date()
    existing_record = HabitRecord.objects.filter(habit=habit, date=today).first()
    if request.method == "POST":
        form = HabitRecordForm(request.POST, metrics=habit.metrics)
        if form.is_valid():
            data = form.cleaned_data
            HabitRecord.objects.update_or_create(
                habit=habit, date=today, defaults={'data': data}
            )
            return redirect('habits:track_habit_detail', habit_id=habit.id)
    else:
        form = HabitRecordForm(metrics=habit.metrics)
    records = HabitRecord.objects.filter(habit=habit).order_by('-date')
    return render(request, 'track_habits/insert_data.html', {
        'habit': habit,
        'form': form,
        'records': records
    })