from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .model import Visit
from .serializer import VisitSerializer

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all().order_by('-created_at')
    serializer_class = VisitSerializer
    permission_classes = [AllowAny]
