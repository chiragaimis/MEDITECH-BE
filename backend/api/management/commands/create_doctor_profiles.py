from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.DoctorProfile.model import DoctorProfile

class Command(BaseCommand):
    help = 'Create DoctorProfile for all users who don\'t have one'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        created_count = 0
        
        for user in users:
            profile, created = DoctorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone': '',
                    'address': '',
                    'specialization': '',
                    'experience': '',
                    'qualification': '',
                    'registration_no': '',
                    'about': ''
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created profile for user: {user.username}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nTotal profiles created: {created_count}')
        )
