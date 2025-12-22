# Accounts App Context

## Overview
This application handles user authentication and role-based access control for the Kitchen Management System. It relies on Django's built-in `User` model and `Group` system rather than a custom user model.

## Key Components

### Models
*   **None defined.** Uses the standard `django.contrib.auth.models.User`.

### Roles & Permissions
The system defines two primary roles, likely managed via Django Groups or `is_staff`/`is_superuser` flags:
1.  **Admin:** Full access to all parts of the system, including user management (`setup_auth` command likely creates these groups).
2.  **Management:** Operational access (Raw Materials, Production, Orders) but restricted from User Management.

### Views & Templates
*   **Login/Logout:** Standard Django auth views, styled with Tailwind.
*   **User Management:** Custom views to list, create, and delete users (Admin only).
*   **Profile:** Simple profile view for the logged-in user.

### Key Files
*   `decorators.py`: Contains custom decorators to enforce role-based access (e.g., `@admin_required`, `@management_required`).
*   `management/commands/setup_auth.py`: Script to initialize groups and permissions.
*   `urls.py`: Routes for login, logout, password change, and user management.

## Developer Notes
*   **No Public Signup:** User accounts are created strictly by internal Admins.
*   **Styling:** Templates use Tailwind CSS to match the project's visual identity.
