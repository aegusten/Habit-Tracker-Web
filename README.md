Habit Tracker Web

Overview
This is a Django web app for building habits, logging daily progress, and earning achievement badges. Users register with an ID number and security questions, create preset or custom habits, log daily metrics, and track streaks, points, and completion status. The UI is server-rendered HTML with a small amount of JavaScript for charts, profile updates, and notifications.

Core Features
- User registration and login using a custom user model keyed by `id_number`.
- Password management with security questions and password change flows.
- Habit creation from presets (stop smoking, wake up early, eat healthy) or custom templates.
- Daily habit logging with metric capture and timeline completion checks.
- Streaks, points, and badges at both user and habit levels.
- Notification messaging and reminders (server-side message generation).

Tech Stack
- Django 3.2 (server-rendered templates)
- PostgreSQL (database)
- Redis (defined in docker-compose, not configured in Django settings)
- Bootstrap 5 via crispy-forms

Project Layout
- `backend/`: primary Django project settings and URLs (used by `manage.py`)
- `accounts/`: custom user model, auth views, and security questions
- `habits/`: habit models, logging, achievements, and tracking views
- `templates/`, `static/`: server-side UI templates and assets
- `docker-compose.yml`, `Dockerfile`: containerized setup

Local Development (manual)
1) Create and activate a virtual environment.
2) Install dependencies:
   `pip install -r requirements.txt`
3) Configure PostgreSQL (see Configuration below).
4) Run migrations:
   `python manage.py migrate`
5) (Optional) Create an admin user:
   `python manage.py createsuperuser`
6) Start the server:
   `python manage.py runserver`
7) Open `http://127.0.0.1:8000/`

Docker Development
1) Ensure Docker and Docker Compose are installed.
2) Create `.env/.postgres` with database values (see Configuration).
3) Build and start services:
   `docker compose up --build`
4) Run migrations inside the web container:
   `docker compose exec web python manage.py migrate`
5) (Optional) Create an admin user:
   `docker compose exec web python manage.py createsuperuser`
6) Open `http://127.0.0.1:8000/`

Configuration
Environment variables are read from `.env/.postgres` when using Docker:
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

The Django settings used by default are in `backend/settings.py`, referenced by `manage.py` via `DJANGO_SETTINGS_MODULE=backend.settings`.

Security Notes
Implemented controls:
- Django authentication with a custom user model (`accounts.User`).
- Password validation rules from Django validators.
- CSRF protection on HTML forms (Django default middleware).
- Route-level access control via `@login_required` for authenticated views.
- Session authentication, with session update on password change.
- Security questions stored per user to support account recovery.

Important operational considerations:
- `DEBUG=True` and hard-coded `SECRET_KEY` are present in `backend/settings.py`. These must be replaced for production.
- `ALLOWED_HOSTS` is empty. Set allowed hosts before deployment.
- Several endpoints are marked `@csrf_exempt` and accept JSON; if exposed publicly, consider CSRF and rate-limiting protections.
- Redis is defined in `docker-compose.yml` but not configured in Django settings.

Backend Routes and APIs
Base URL: `/`

HTML routes (server-rendered):
- `GET /` -> login page (same as `/accounts/`)
- `GET /admin/` -> Django admin
- `GET /accounts/` -> login page
- `GET /accounts/register/` -> registration page
- `POST /accounts/register/` -> register and log in
- `GET /accounts/login/` -> login page
- `POST /accounts/login/` -> log in
- `GET /accounts/logout/` -> log out
- `GET /accounts/main_menu/` -> main menu dashboard
- `GET /accounts/edit_personal_info/` -> edit profile + badges view
- `POST /accounts/edit_personal_info/` -> update profile
- `GET /accounts/profile/` -> profile view (uses edit template)
- `GET /habits/new/` -> habit creation form
- `POST /habits/new/` -> create habit
- `GET /habits/ongoing/` -> list ongoing habits
- `GET /habits/track/<habit_id>/` -> habit detail and stats
- `POST /habits/track/<habit_id>/` -> update reminder or timeline
- `GET /habits/insert/<habit_id>/` -> daily log form
- `POST /habits/insert/<habit_id>/` -> submit daily log
- `GET /habits/abort/<habit_id>/` -> delete habit and return to ongoing list
- `GET /habits/notifications/` -> notification dashboard

JSON APIs:
- `POST /accounts/public_forgot_password/`
  - Body: JSON with `id_number` plus either password verification fields or password change fields.
  - Returns: `{ok: true}` or `{ok: false, errors: {...}}`.
- `POST /accounts/public_verify_security_answers/`
  - Body: JSON with `id_number` and answers keyed by question id.
  - Returns: `{valid: true|false}`.
- `POST /accounts/change_password/` (requires login)
  - Body: JSON, supports password verification or change flow.
  - Returns: `{ok: true}` or `{ok: false, errors: {...}}`.
- `POST /accounts/get_security_questions/`
  - Body: JSON with `id_number`.
  - Returns: `{questions: [{id, text}, ...]}`.
- `POST /habits/notifications/push/` (requires login)
  - Body: form-encoded `habit_type` and `stage`.
  - Returns: `{message: "..."}`.
- `POST /habits/api/save-custom-data/<habit_id>/` (requires login)
  - Body: JSON numeric field updates for custom habits only.
  - Returns: `{success: true}` or `{error: "..."}`.
- `GET /habits/api/record/<record_id>/` (requires login)
  - Returns: `{id, date, data}`.

Notes on data:
- Habit metrics are stored in JSON on the `Habit` record (`metrics`) and daily logs are stored in `HabitRecord.data`.
- Preset habits store predefined metrics (stop smoking, wake up early, eat healthy).

Tests
There are no automated tests configured in this repository.
