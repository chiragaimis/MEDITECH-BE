from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create superuser if not exists'

    def handle(self, *args, **kwargs):
        username = "admin"
        email = "admin@gmail.com"
        password = "Welcome@1"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS("Superuser created successfully"))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists"))