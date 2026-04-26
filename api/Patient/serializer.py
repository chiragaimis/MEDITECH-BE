from rest_framework import serializers
from api.Patient.model import Patient
from api.Visit.serializer import VisitSerializer


class PatientSerializer(serializers.ModelSerializer):
    visits = VisitSerializer(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ("id", "patient_id", "created_at")
