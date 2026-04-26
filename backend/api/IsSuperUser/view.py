from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class CheckUserType(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        user_groups = user.groups.all()
        role_names = [group.name for group in user_groups]
        # Add "superuser" if the user is a superuser
        if user.is_superuser:
            role_names.append("superuser")
        if not role_names:
            role_names = ["No Role Assigned"]

        return Response({"roles": role_names})