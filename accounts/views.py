from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
import json
from .forms import RegisterForm, LoginForm, UpdatePersonalInfoForm

def index_view(request):
    return redirect('accounts:login')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:main_menu')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('accounts:main_menu')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'register_form': RegisterForm()})

@login_required
def main_menu_view(request):
    return render(request, 'main_menu.html')

@login_required
def edit_personal_info_view(request):
    user = request.user
    form = UpdatePersonalInfoForm(request.POST or None, instance=user)
    password_form = PasswordChangeForm(user=user)
    reset_form = SetPasswordForm(user=user)
    forgot = 'forgot' in request.POST
    verify = 'verify' in request.POST

    security_questions = {
        "What was your first pet’s name?": user.pet_name,
        "Who was your first love?": user.first_love,
    }
    security_questions = {q: a for q, a in security_questions.items() if a}

    if verify:
        answers = {q: request.POST.get(q) for q in security_questions}
        if all(answers[q].strip().lower() == security_questions[q].lower() for q in security_questions):
            password_form = reset_form
            forgot = False

    if request.method == 'POST' and form.is_valid() and not forgot and not verify:
        form.save()
        return redirect('accounts:main_menu')

    return render(request, 'edit_personal_info.html', {
        'form': form,
        'password_form': password_form,
        'security_questions': security_questions,
        'forgot': forgot,
    })

@login_required
def verify_password(request):
    data = json.loads(request.body)
    valid = authenticate(request, username=request.user.id_number, password=data.get('old_password')) is not None
    return JsonResponse({'valid': valid})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return redirect('accounts:main_menu')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')
