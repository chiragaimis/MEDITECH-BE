from rest_framework import serializers
from api.Symptom.model import Symptom


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = "__all__"
     
