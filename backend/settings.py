import os
from pathlib import Path
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

DEMO_MODE = os.getenv('DEMO_MODE') == 'True'

SECRET_KEY = 'a-strong-secret-key'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_celery_beat',
    'django_celery_results',
    
    'accounts',
    'habits',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_DIRS = [ BASE_DIR / "static" ]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'habit_db'),
        'USER': os.environ.get('POSTGRES_USER', 'habit_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'habit_password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'


if DEMO_MODE:
    CELERY_BEAT_SCHEDULE = {
        # Fires 1 minute after habit creation
        'demo_initial_reminder': {
            'task': 'habits.tasks.send_notification',
            'schedule': crontab(minute='*/1'),
            'args': ('Welcome to your new habit!',)
        },
        # Fires 2 minutes in → Daily Reminder
        'demo_daily_reminder': {
            'task': 'habits.tasks.send_notification',
            'schedule': crontab(minute='*/2'),
            'args': ('Daily Check‑In: Keep going!',)
        },
        # Fires 3 minutes in → Weekly Reminder
        'demo_weekly_reminder': {
            'task': 'habits.tasks.send_notification',
            'schedule': crontab(minute='*/3'),
            'args': ('Weekly Motivation: You’re doing great!',)
        },
        # Fires 4 minutes in → Upcoming Challenge
        'demo_challenge': {
            'task': 'habits.tasks.send_notification',
            'schedule': crontab(minute='*/4'),
            'args': ('Next badge in 1 day — keep your streak alive!',)
        },
        # Fires 5 minutes in → Badge Earned
        'demo_badge': {
            'task': 'habits.tasks.send_notification',
            'schedule': crontab(minute='*/5'),
            'args': ('🏅 Congrats — Silver Badge Unlocked!',)
        },
        # Fires 6 minutes in → Streak Broken
        'demo_streak_break': {
            'task': 'habits.tasks.send_notification',
            'schedule': crontab(minute='*/6'),
            'args': ('⚠️ Oops — your streak reset to 0',)
        },
    }

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
