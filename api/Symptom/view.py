from rest_framework.viewsets import ModelViewSet
from api.Symptom.model import Symptom
from api.Symptom.serializer import SymptomSerializer


class SymptomViewSet(ModelViewSet):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
