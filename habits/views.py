from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import HabitForm, HabitRecordForm
from .models import Habit, HabitRecord

PRESET_HABITS = {
    'stop_smoking': {
        'metrics': {'cigarettes_per_day':0, 'days_smoke_free':0, 'money_saved':0, 'craving_intensity':0},
        'targets': {'cigarettes_per_day':0}
    },
    'wake_up_early': {
        'metrics': {'wake_time':None, 'bedtime':None, 'sleep_duration':0, 'streak_count':0},
        'targets': {'wake_time': '06:00'}
    },
    'eat_healthy': {
        'metrics': {'meals_logged':0, 'fruit_veg_servings':0, 'water_glasses':0, 'hunger_rating':0},
        'targets': {'fruit_veg_servings':5}
    }
}

PRESET_TEMPLATES = [
    {'key':'stop_smoking','icon':'bi-emoji-smile','label':'Stop Smoking'},
    {'key':'wake_up_early','icon':'bi-sunrise','label':'Wake Up Early'},
    {'key':'eat_healthy','icon':'bi-apple','label':'Eat Healthy'},
    {'key':'custom','icon':'bi-pencil-square','label':'Custom'},
]

@login_required
def form_new_habit_view(request):
    template_key = request.GET.get('template')
    initial = PRESET_HABITS.get(template_key, {}) if template_key else {}
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            if template_key in PRESET_HABITS:
                habit.metrics = PRESET_HABITS[template_key]['metrics']
                habit.targets = PRESET_HABITS[template_key]['targets']
            habit.save()
            return redirect('habits:ongoing_habit')
    else:
        form = HabitForm(initial=initial)
    return render(request, 'form_new_habit.html', {'form': form, 'templates': PRESET_TEMPLATES})

@login_required
def ongoing_habit_view(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'ongoing_habit.html', {'habits': habits})

@login_required
def track_habit_view(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == 'POST':
        form = HabitRecordForm(request.POST, metrics=habit.metrics)
        if form.is_valid():
            HabitRecord.objects.update_or_create(
                habit=habit,
                date=form.cleaned_data.get('date') or timezone.now().date(),
                defaults={'data': form.cleaned_data}
            )
            return redirect('habits:track_habit', habit_id=habit.id)
    else:
        form = HabitRecordForm(metrics=habit.metrics)
    records = HabitRecord.objects.filter(habit=habit).order_by('-date')
    return render(request, 'track_habit.html', {'habit': habit, 'form': form, 'records': records})

@login_required
def abort_process_view(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.delete()
    return redirect('habits:ongoing_habit')