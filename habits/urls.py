from django.urls import path
from . import views

app_name = 'habits'

urlpatterns = [
    path('new/', views.form_new_habit_view, name='form_new_habit'),
    path('ongoing/', views.ongoing_habit_view, name='ongoing_habit'),
    path('abort/<int:habit_id>/', views.abort_process_view, name='abort_process'),
    path('track/<int:habit_id>/', views.track_habit_detail_view, name='track_habit_detail'),
    path('insert/<int:habit_id>/', views.insert_data_view, name='insert_data'),
    
    path('notifications/', views.notification_dashboard_view, name='notification_dashboard'),
    path('notifications/push/', views.push_notification, name='push_notification')
]
