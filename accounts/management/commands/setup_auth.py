import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Set up authentication groups and create default admin user'

    def handle(self, *args, **options):
        # Create groups
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created Admin group'))
        else:
            self.stdout.write('Admin group already exists')

        management_group, created = Group.objects.get_or_create(name='Management')
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created Management group'))
        else:
            self.stdout.write('Management group already exists')

        # Create default admin user
        username = 'admin'
        email = 'admin@kitchen.local'
        password = os.getenv('ADMIN_DEFAULT_PASSWORD', 'admin123456')  # Change in production

        try:
            if not User.objects.filter(username=username).exists():
                admin_user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    first_name='Admin',
                    last_name='User'
                )
                admin_user.groups.add(admin_group)
                admin_user.save()

                self.stdout.write(self.style.SUCCESS(f'✓ Created default admin user'))
                self.stdout.write(self.style.WARNING(f'  Username: {username}'))
                self.stdout.write(self.style.WARNING(f'  Password: {password}'))
                self.stdout.write(self.style.WARNING('  ⚠️  Please change the password immediately!'))
            else:
                self.stdout.write('Default admin user already exists')

        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating admin user: {e}'))

        self.stdout.write(self.style.SUCCESS('\n✓ Authentication setup complete'))
