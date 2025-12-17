from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class UserProfile(models.Model):
    """Track user-specific settings including tutorial completion status."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    tutorial_completed = models.BooleanField(default=False)
    tutorial_completed_at = models.DateTimeField(null=True, blank=True)
    tutorial_dismissed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f"Profile for {self.user.username}"


# Auto-create profile for new users
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a UserProfile when a User is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Automatically save UserProfile when User is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
