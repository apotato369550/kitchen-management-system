from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create default user groups (Admin and Management)'

    def handle(self, *args, **options):
        groups_data = {
            'Admin': [],
            'Management': [],
        }

        for group_name, permissions in groups_data.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {group_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Group already exists: {group_name}'))

        self.stdout.write(self.style.SUCCESS('Groups setup complete'))
