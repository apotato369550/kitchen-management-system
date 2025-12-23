from functools import wraps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


def is_admin(user):
    """Check if user is in Admin group or is a superuser"""
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Admin').exists())


def is_management(user):
    """Check if user is in Management group"""
    return user.is_authenticated and user.groups.filter(name='Management').exists()


def is_viewer(user):
    """Check if user is in Viewer group (read-only access)"""
    return user.is_authenticated and user.groups.filter(name='Viewer').exists()


def admin_required(view_func):
    """Decorator to require admin group membership"""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not is_admin(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def management_or_admin_required(view_func):
    """Decorator to require Management or Admin group membership"""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not (is_admin(request.user) or is_management(request.user)):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper
