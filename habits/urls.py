from django.urls import path
from . import views

app_name = 'habits'

urlpatterns = [
    path('new/', views.form_new_habit_view, name='form_new_habit'),
    path('ongoing/', views.ongoing_habit_view, name='ongoing_habit'),
    path('track/<int:habit_id>/', views.track_habit_view, name='track_habit'),
    path('abort/<int:habit_id>/', views.abort_process_view, name='abort_process'),
    path('track_habit/<int:habit_id>/', views.track_habit_detail_view, name='track_habit_detail'),
    
    path('track/<int:habit_id>/streaks/', views.view_streaks, name='view_streaks'),
    path('track/<int:habit_id>/points/', views.view_points, name='view_points'),
    path('track/<int:habit_id>/challenges/', views.upcoming_challenges, name='upcoming_challenges'),
    path('track/<int:habit_id>/insights/', views.view_insights, name='view_insights'),
    path('track/<int:habit_id>/reminders/', views.update_reminders, name='update_reminders'),
    path('track/<int:habit_id>/goal/', views.update_goal, name='update_goal'),
]
