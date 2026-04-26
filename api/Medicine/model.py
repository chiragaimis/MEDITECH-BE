import uuid
from api.Symptom.model import Symptom
from django.db import models


class Medicine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medicine_name = models.CharField(max_length=255, unique=True, null = True, blank=True)
    full_description = models.TextField()
    dose = models.CharField(max_length=255, blank=True, null=True)
   

    def __str__(self):
        return self.medicine_name