from rest_framework.viewsets import ModelViewSet
from api.Patient.model import Patient
from api.Patient.serializer import PatientSerializer
from rest_framework.permissions import AllowAny

class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all().order_by("-created_at")
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]
