from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.login_view, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('main_menu/', views.main_menu_view, name='main_menu'),
    path('edit_personal_info/', views.edit_personal_info_view, name='edit_personal_info'),
    path('change_password/', views.change_password_view, name='change_password'),
    path('public_forgot_password/', views.public_forgot_password_view, name='public_forgot_password_view'),
    path('public_verify_security_answers/', views.public_verify_security_answers, name='public_verify_security_answers'),
    path('profile/', views.profile_view, name='profile'),
    path('accounts/get_security_questions/', views.get_security_questions_view, name='get_security_questions')
]