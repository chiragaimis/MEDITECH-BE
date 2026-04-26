from rest_framework import serializers
from .model import MedicineSymptom


class MedicineSymptomSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.medicine_name', read_only=True)
    symptom_name = serializers.CharField(source='symptom.symptom_name', read_only=True)
    
    class Meta:
        model = MedicineSymptom
        fields = ['id', 'medicine', 'symptom', 'confidence_level', 'medicine_name', 'symptom_name']