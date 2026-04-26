from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.DoctorProfile.model import DoctorProfile
from api.DoctorProfile.serializer import DoctorProfileSerializer, DoctorProfileUpdateSerializer

class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get', 'put', 'patch'], url_path='me')
    def get_my_profile(self, request):
        """Get or Update current logged-in doctor's profile"""
        # Auto-create profile if doesn't exist
        profile, created = DoctorProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'phone': '',
                'address': '',
                'specialization': '',
                'experience': '',
                'qualification': '',
                'registration_no': '',
                'about': ''
            }
        )
        
        # GET request - return profile
        if request.method == 'GET':
            serializer = DoctorProfileSerializer(profile)
            return Response(serializer.data)
        
        # PUT/PATCH request - update profile
        serializer = DoctorProfileUpdateSerializer(
            profile, 
            data=request.data, 
            partial=request.method == 'PATCH'
        )
        
        if serializer.is_valid():
            serializer.save()
            response_serializer = DoctorProfileSerializer(profile)
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='me/delete')
    def delete_my_profile(self, request):
        """Delete current logged-in doctor's profile"""
        try:
            profile = DoctorProfile.objects.get(user=request.user)
            profile.delete()
            return Response(
                {"message": "Profile deleted successfully"},
                status=status.HTTP_200_OK
            )
        except DoctorProfile.DoesNotExist:
            return Response(
                {"error": "Doctor profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )
