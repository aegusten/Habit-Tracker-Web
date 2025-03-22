from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.login_view, name='root'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('habits/', include('habits.urls', namespace='habits')),
]
