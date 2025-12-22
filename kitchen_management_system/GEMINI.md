# Project Configuration Context

## Overview
This directory contains the global configuration for the Django project.

## Key Files
*   `settings.py`: The heart of the configuration.
    *   **Apps:** `core`, `accounts`, `django_axes`, `whitenoise`.
    *   **Database:** Configured to use `dj_database_url` for parsing Supabase connection strings.
    *   **Security:** `SECRET_KEY` and `DEBUG` controlled via `.env`.
    *   **Static Files:** WhiteNoise is configured for serving static assets in production.
*   `urls.py`: The root URL router. It delegates traffic to `core.urls` and `accounts.urls`.
*   `wsgi.py` / `asgi.py`: Entry points for web servers (Gunicorn/Vercel).

## Environment Variables
Ensure `.env` matches the variables expected in `settings.py`. Crucially:
*   `SUPABASE_...` variables for DB connection.
*   `SECRET_KEY`
*   `DEBUG`
