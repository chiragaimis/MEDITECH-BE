import uuid
from django.db import models
from django.contrib.auth.models import User

class DoctorProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    
    # Basic Info
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = models.TextField(blank=True, null=True)  # Base64 or URL
    
    # Professional Info
    specialization = models.CharField(max_length=255, blank=True, null=True)
    experience = models.CharField(max_length=50, blank=True, null=True)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    registration_no = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username}"
