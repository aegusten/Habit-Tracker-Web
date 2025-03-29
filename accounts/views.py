from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.http import JsonResponse
from habits.models import Habit
from django.contrib import messages

from django.contrib.auth.forms import (
    PasswordChangeForm,
    SetPasswordForm,
)

from .models import (
    UserSecurityAnswer,
    SecurityQuestion,
    User,
)

from habits.utils import (
    PRESET_HABITS,
    PRESET_TEMPLATES,
    AWARD_MESSAGES,
    NOTIFICATION_MESSAGES,
    get_notification_message,
    get_random_reminder
)

import json
from .forms import RegisterForm, LoginForm, UpdatePersonalInfoForm

def index_view(request):
    return redirect('accounts:login')

@login_required
def main_menu_view(request):
    user = request.user
    habits = Habit.objects.filter(user=user)

    habit_summary = {
        'daily': [],
        'weekly': []
    }

    for habit in habits:
        habit_type = habit.template_key or 'custom'
        reminder = habit.motivational_reminder
        print(f"[DEBUG] Habit: {habit.name}, Type: {habit_type}, Reminder: {reminder}")

        if reminder == 'daily':
            habit_summary['daily'].append(habit_type)
        elif reminder == 'weekly':
            habit_summary['weekly'].append(habit_type)

    habit_summary['daily'] = list(set(habit_summary['daily']))
    habit_summary['weekly'] = list(set(habit_summary['weekly']))

    print(f"[SUMMARY] Total Habits: {habits.count()}")
    print(f"[SUMMARY] Daily Types: {habit_summary['daily']}")
    print(f"[SUMMARY] Weekly Types: {habit_summary['weekly']}")

    return render(request, 'main_menu.html', {
        'daily_habit_types': habit_summary['daily'],
        'weekly_habit_types': habit_summary['weekly'],
        'habit_count': habits.count(),
    })

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            q_obj1 = get_object_or_404(SecurityQuestion, question_text="Security Question 1")
            chosen_q1 = form.cleaned_data['question1_subquestion'] 
            ans1 = form.cleaned_data['answer1']
            UserSecurityAnswer.objects.create(
                user=user,
                question=q_obj1,
                question_text=chosen_q1,
                answer=ans1
            )
            
            q_obj2 = get_object_or_404(SecurityQuestion, question_text="Security Question 2")
            chosen_q2 = form.cleaned_data['question2_subquestion']
            ans2 = form.cleaned_data['answer2']
            UserSecurityAnswer.objects.create(
                user=user,
                question=q_obj2,
                question_text=chosen_q2,
                answer=ans2
            )
            
            chosen_q3 = form.cleaned_data.get('question3_subquestion')
            ans3 = form.cleaned_data.get('answer3')
            if chosen_q3 and ans3:
                q_obj3 = get_object_or_404(SecurityQuestion, question_text="Security Question 3")
                UserSecurityAnswer.objects.create(
                    user=user,
                    question=q_obj3,
                    question_text=chosen_q3,
                    answer=ans3
                )
            
            login(request, user)
            return redirect('accounts:main_menu')
    else:
        form = RegisterForm()
    return render(request, 'login.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('accounts:main_menu')
    else:
        form = LoginForm()
    register_form = RegisterForm()
    return render(request, 'login.html', {'form': form, 'register_form': register_form})

def public_forgot_password_view(request):
    data = json.loads(request.body)
    id_number = data.get('id_number', '').strip()
    user = User.objects.filter(id_number=id_number).first()
    if not user:
        return JsonResponse({"ok": False, "errors": {"id_number": ["User not found."]}}, status=400)
    if data.get('verify'):
        form = SetPasswordForm(user, data)
        if form.is_valid():
            form.save()
            return JsonResponse({"ok": True})
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)
    old_password = data.get("old_password", "").strip()
    new_password1 = data.get("new_password1", "").strip()
    new_password2 = data.get("new_password2", "").strip()
    if 'old_password' in data and (new_password1 or new_password2):
        if not user.check_password(old_password):
            return JsonResponse({"ok": False, "errors": {"old_password": ["Incorrect password."]}}, status=400)
        if old_password == new_password1:
            return JsonResponse({"ok": False, "errors": {"new_password1": ["New password cannot be the same as the old password."]}}, status=400)
        form = PasswordChangeForm(user, data)
        if form.is_valid():
            form.save()
            return JsonResponse({"ok": True})
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)
    if old_password:
        if not user.check_password(old_password):
            return JsonResponse({"ok": False, "errors": {"old_password": ["Incorrect password."]}}, status=400)
        return JsonResponse({"ok": True})
    return JsonResponse({"error": "Invalid request"}, status=400)

def public_verify_security_answers(request):
    data = json.loads(request.body)
    id_number = data.get('id_number', '').strip()
    user = User.objects.filter(id_number=id_number).first()
    if not user:
        return JsonResponse({'valid': False})
    user_answers = UserSecurityAnswer.objects.filter(user=user)
    correct = 0
    for ua in user_answers:
        typed = data.get(ua.question_text, '').strip().lower()
        if ua.answer.strip().lower() == typed:
            correct += 1
    return JsonResponse({'valid': correct >= 2})


@login_required
def change_password_view(request):
    user = request.user
    data = json.loads(request.body)

    if data.get('verify'):
        form = SetPasswordForm(user, data)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            return JsonResponse({"ok": True})
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)

    if (
        'old_password' in data
        and data.get('new_password1') == ""
        and data.get('new_password2') == ""
    ):
        old_password = data["old_password"].strip()
        print("DEBUG old_password:", repr(old_password))
        print("DEBUG check_password =>", user.check_password(old_password))
        if not user.check_password(old_password):
            return JsonResponse({"ok": False, "errors": {"old_password": ["Incorrect password."]}}, status=400)
        return JsonResponse({"ok": True})

    if 'old_password' in data and data.get('old_password'):
        form = PasswordChangeForm(user, data)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            return JsonResponse({"ok": True})
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def edit_personal_info_view(request):
    user = request.user
    form = UpdatePersonalInfoForm(request.POST or None, instance=user)
    password_form = PasswordChangeForm(user=user)
    set_password_form = SetPasswordForm(user=user)
    user_answers = user.security_answers.all()
    questions = {ua.question_text: ua.answer for ua in user_answers}
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('accounts:edit_personal_info')
    context = {
        'form': form,
        'password_form': password_form,
        'set_password_form': set_password_form,
        'security_questions': questions,
    }
    return render(request, 'edit_personal_info.html', context)

@login_required
def verify_security_answers(request):
    data = json.loads(request.body)
    user = request.user
    user_answers = user.security_answers.all()
    correct = 0
    for ua in user_answers:
        submitted = data.get(ua.question_text, "").strip().lower()
        if ua.answer.strip().lower() == submitted:
            correct += 1
    return JsonResponse({'valid': correct >= 2})
