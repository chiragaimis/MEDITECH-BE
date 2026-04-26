from rest_framework import viewsets
from .model import MedicineSymptom
from .serializer import MedicineSymptomSerializer


class MedicineSymptomViewSet(viewsets.ModelViewSet):
    queryset = MedicineSymptom.objects.all()
    serializer_class = MedicineSymptomSerializer