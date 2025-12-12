# Django Initialization Plan

## Goal
Set up a minimal Django project with a "Hello World" page, configured for Supabase PostgreSQL.

## Steps

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install django psycopg2-binary python-dotenv
```

### 3. Create Django Project
```bash
django-admin startproject kitchen_project .
```

### 4. Create Core App
```bash
python manage.py startapp core
```

### 5. Configure Settings
- Add `core` to `INSTALLED_APPS`
- Configure database to use Supabase PostgreSQL via environment variables:
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'postgres',
          'USER': 'postgres',
          'PASSWORD': os.getenv('SUPABASE_PROJECT_PASSWORD'),
          'HOST': '<project-ref>.supabase.co',
          'PORT': '5432',
      }
  }
  ```
- Load `.env` with python-dotenv

### 6. Create Hello World View
In `core/views.py`:
```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World")
```

### 7. Configure URLs
- `kitchen_project/urls.py` includes `core.urls`
- `core/urls.py` maps `/` to index view

### 8. Run & Verify
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` → should display "Hello World"

## File Structure After Init
```
kitchen-management-system/
├── venv/
├── kitchen_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── manage.py
├── .env
└── requirements.txt
```
