from rest_framework import serializers
from .model import Medicine

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = "__all__"


class MedicineSuggestionSerializer(serializers.Serializer):
    symptoms = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )