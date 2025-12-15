# Project Settings - CLAUDE.md

## Purpose

This directory contains Django project configuration and settings.

## Structure

```
kitchen_management_system/
├── __init__.py
├── asgi.py              # ASGI configuration for async support
├── settings.py          # Main Django settings
├── urls.py              # Root URL configuration
└── wsgi.py              # WSGI configuration for deployment
```

## Settings Configuration

### Database
- Uses PostgreSQL via Supabase connection pooler
- Connection details loaded from environment variables
- Configured for IPv4 connectivity

### Security Settings
- `SECRET_KEY`: Django secret key (from env variable)
- `DEBUG`: Should be False in production
- CSRF protection enabled
- Session security configured

### Installed Apps
- Django built-in apps (admin, auth, contenttypes, sessions, messages, staticfiles)
- `core` - Main application
- `accounts` - Authentication app (to be added)

### Middleware
- Standard Django middleware stack
- CSRF, sessions, authentication, messages

### Database Configuration
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': os.getenv('SUPABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('SUPABASE_PROJECT_PASSWORD'),
        'HOST': os.getenv('SUPABASE_HOST', 'localhost'),
        'PORT': os.getenv('SUPABASE_PORT', '5432'),
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}
```

### Static Files
- `STATIC_URL`: '/static/'
- Configure `STATIC_ROOT` for production

### Templates
- Django template engine
- Template directories to be configured per app

## URL Configuration

Root URL patterns in `urls.py`:
- `/admin/` - Django admin interface
- `/` - Includes core app URLs
- `/accounts/` - Authentication URLs (to be added)

## Production Settings

For Vercel deployment, update:
- `ALLOWED_HOSTS` - Add production domain
- `DEBUG = False`
- `SECURE_SSL_REDIRECT = True`
- `SESSION_COOKIE_SECURE = True`
- `CSRF_COOKIE_SECURE = True`
- Configure static file serving

## Environment Variables

Required variables:
- `SUPABASE_PROJECT_PASSWORD`
- `SUPABASE_HOST`
- `SUPABASE_PORT`
- `SUPABASE_USER`
- `SECRET_KEY`
- `DEBUG`

## Security Considerations

1. Never commit secrets or passwords
2. Use strong SECRET_KEY in production
3. Enable HTTPS in production
4. Configure CORS properly
5. Set secure cookie flags
6. Use environment variables for all sensitive data

## Development vs Production

### Development
- `DEBUG = True`
- Detailed error pages
- Django development server
- SQLite can be used for local testing
- Relaxed CORS settings

### Production
- `DEBUG = False`
- Generic error pages
- WSGI server (Gunicorn/uWSGI)
- PostgreSQL (Supabase)
- Strict CORS settings
- HTTPS required
- Secure cookies

## Database Migrations

Always run migrations after settings changes:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Custom Settings (Future)

Consider splitting settings into:
- `base.py` - Common settings
- `development.py` - Dev-specific
- `production.py` - Prod-specific

## Logging Configuration

Add logging configuration for production:
- Error logs
- Access logs
- Database query logs (development only)
