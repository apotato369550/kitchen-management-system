# Authentication System Plan

## Goal
Implement a secure, admin-controlled authentication system using Django's built-in auth. No public signup - only admins can create user accounts.

## Security Requirements
- Secure password hashing (Django's default PBKDF2)
- CSRF protection (Django middleware)
- Session security with secure cookies in production
- Login throttling to prevent brute force attacks
- HTTPS enforcement in production (Vercel)
- Strong password validation

## User Roles

### Admin
- Full system access
- Can create, edit, and delete user accounts
- Can manage all data (raw materials, production, purchase orders)
- Access to user management panel

### Management (Owner & Secretary)
- Can manage daily operations
- Access to raw materials tracker
- Access to production tracker
- Access to purchase order tracker
- Cannot create or manage user accounts

## Implementation Steps

### 1. Create Custom User Model (Optional but Recommended)
While Django's default User model works, a custom user model provides flexibility.
- Extend `AbstractUser` or use default `User` model
- Add `role` field: choices=['admin', 'management']
- Decision: Use default User model with groups for simplicity

### 2. Configure User Groups & Permissions
Create two groups in Django:
- **Admin Group**: Full permissions
- **Management Group**: Limited permissions (no user management)

### 3. Create User Management Views (Admin Only)
In a new app `accounts/`:
- List users view
- Create user view (form with username, password, role)
- Edit user view
- Delete user view (with confirmation)
- Restrict all views to admin group

### 4. Implement Login/Logout
- Login view with username/password
- Logout view
- Login required decorator for all app views
- Redirect after login based on role

### 5. Create Default Admin Account
- Management command or migration to create default admin
- Username: `admin`
- Password: Set securely (prompt during setup or via environment variable)

### 6. Security Hardening
- Configure settings for production:
  ```python
  # Session security
  SESSION_COOKIE_SECURE = True  # HTTPS only
  SESSION_COOKIE_HTTPONLY = True
  CSRF_COOKIE_SECURE = True
  SECURE_SSL_REDIRECT = True
  SECURE_HSTS_SECONDS = 31536000

  # Password validation
  AUTH_PASSWORD_VALIDATORS = [
      {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
      {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 10}},
      {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
      {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
  ]
  ```
- Install and configure `django-axes` for login throttling
- Set `ALLOWED_HOSTS` properly for production

### 7. Create Login UI
- Simple, clean login page (Tailwind CSS)
- Error messages for invalid credentials
- "Remember me" checkbox (optional)
- Password reset functionality (optional, future)

### 8. Implement Permission Checks
- Decorator for admin-only views: `@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())`
- Template tags to show/hide UI elements based on permissions
- Middleware to check user role on each request

## File Structure After Implementation
```
kitchen-management-system/
├── accounts/                      # New app for authentication
│   ├── migrations/
│   ├── templates/
│   │   └── accounts/
│   │       ├── login.html
│   │       ├── user_list.html
│   │       ├── user_form.html
│   │       └── user_confirm_delete.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── decorators.py             # Custom permission decorators
│   ├── forms.py                   # User creation/edit forms
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── management/
│       └── commands/
│           └── create_default_admin.py
├── core/
├── kitchen_management_system/
│   └── settings.py               # Updated with security settings
└── requirements.txt              # Add django-axes
```

## Testing Checklist
- [ ] Admin can log in
- [ ] Admin can create management users
- [ ] Management users can log in
- [ ] Management users cannot access user management
- [ ] Failed login attempts are rate-limited
- [ ] Sessions expire after inactivity
- [ ] HTTPS redirect works in production
- [ ] CSRF tokens are present on all forms

## Dependencies to Add
```
django-axes>=6.0.0  # Login throttling
```

## Notes
- Keep authentication simple - use Django's battle-tested auth system
- Don't overcomplicate with Supabase Auth for this use case
- Focus on security: HTTPS, secure sessions, rate limiting
- Default admin password should be changed on first login
