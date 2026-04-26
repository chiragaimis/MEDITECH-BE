import uuid
import random
from django.db import models

GENDER_CHOICES = [
    ('Male', 'male  '),
    ('Female', 'female'),
    ('Other', 'other'), 
]
def generate_unique_patient_id():
    while True:
        pid = random.randint(100000, 999999)  # 6-digit numeric ID
        if not Patient.objects.filter(patient_id=pid).exists():
            return pid


class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_id = models.IntegerField(unique=True, default=generate_unique_patient_id)

    name = models.CharField(max_length=150,blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.patient_id})"
