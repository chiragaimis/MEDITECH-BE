#api/Symptom/model.py
import uuid
from django.db import models



class Symptom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    symptom_name = models.CharField(max_length=255, null =True, blank=True)
    normalized_name = models.CharField(max_length=255, unique=True, null =True)
    body_part = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.normalized_name = self.symptom_name.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.symptom_name