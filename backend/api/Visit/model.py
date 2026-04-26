from django.db import models
from api.Patient.model import Patient
import uuid
from django.contrib.postgres.fields import ArrayField

class Visit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="visits")
    visit_date = models.DateField()
    diagnosis = models.CharField(max_length=255)
    symptoms = models.TextField()

    medicines = ArrayField(models.CharField(max_length=255), blank=True, default=list)

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visit of {self.patient.name} on {self.visit_date}"
