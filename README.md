# BGHI7

University-only community app (students + alumni) built with Django.

## Requirements

- Python 3.10+ (recommended)
- macOS / Linux / Windows

## Setup (first time)

From the project root:

1) Create and activate a virtual environment

- macOS/Linux:
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`

- Windows (PowerShell):
  - `py -m venv .venv`
  - `.\.venv\Scripts\Activate.ps1`

2) Install dependencies

- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`

3) Run migrations

- `python manage.py migrate`

4) (Optional) Seed demo data

- `python manage.py seed_demo_data --yes`

This creates demo users and sample posts/comments.

5) Start the server

- `python manage.py runserver`

Open `http://127.0.0.1:8000/`.

## Demo accounts

If you ran `seed_demo_data`, use:

- Student:
  - `student1@th-deg.de` / `student123`
  - `student2@th-deg.de` / `student123`
- Alumni:
  - `alumni1@gmail.com` / `alumni123`

## Admin / Django shell

Create an admin user:

- `python manage.py createsuperuser`

Open admin:

- `http://127.0.0.1:8000/admin/`

## Notes

- Local SQLite DB (`db.sqlite3`) is intentionally not committed. Each developer will create their own via `migrate`.
- Student registration is gated by the configured university email domain in settings (`UNIVERSITY_EMAIL_DOMAIN`).
- The “Jobs & Referrals” topic is demo-gated by `User.is_paid`.

## API

- API routes are mounted at `/api/` (see `GET /api`).
- Most API endpoints require authentication (`IsAuthenticated`). The simplest way in local dev is to log in via the web UI first, then call the API using the same session/cookies.
