from rest_framework import serializers
from api.DoctorProfile.model import DoctorProfile
from django.contrib.auth.models import User

class DoctorProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = DoctorProfile
        fields = [
            'id', 'name', 'email', 'phone', 'address', 'profile_image',
            'specialization', 'experience', 'qualification', 
            'registration_no', 'about', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class DoctorProfileUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    
    class Meta:
        model = DoctorProfile
        fields = [
            'name', 'email', 'phone', 'address', 'profile_image',
            'specialization', 'experience', 'qualification', 
            'registration_no', 'about'
        ]
    
    def update(self, instance, validated_data):
        # Update User fields
        user = instance.user
        if 'name' in validated_data:
            name_parts = validated_data.pop('name').split(' ', 1)
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        if 'email' in validated_data:
            user.email = validated_data.pop('email')
        user.save()
        
        # Update DoctorProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance
