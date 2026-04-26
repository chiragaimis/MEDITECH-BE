import uuid
from django.db import models
from api.Medicine.model import Medicine
from api.Symptom.model import Symptom

class MedicineSymptom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE,null = True, blank=True)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE,null = True, blank=True)
    confidence_level = models.CharField(max_length=20,choices=[("primary", "Primary"), ("secondary", "Secondary")],default="primary")

    class Meta:
        unique_together = ("medicine", "symptom")