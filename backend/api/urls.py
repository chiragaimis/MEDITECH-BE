
from django.contrib import admin
from django.urls import path,include
from api.Permission import view as permissionView
from api.Role import view as roleView
from api.User import view as userView

from api.ChangeMyPassword.view import ChangeMyPasswordView
from api.ForgetPassword.view import PasswordResetRequestView
from api.IsSuperUser.view import CheckUserType
from api.CreateUser import views as createUserViews
from api.Patient import view as patientView
from api.Visit import view as visitView
from api.Symptom.view import SymptomViewSet
from api.Medicine.view import MedicineViewSet
from api.MedicineSymtom.view import MedicineSymptomViewSet
from api.DoctorProfile.view import DoctorProfileViewSet
from api.CustomAPI.dashboard import DashboardView

from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router=routers.DefaultRouter()
router.register(r'user',userView.UserViewset, basename='user'),
router.register(r'role',roleView.RoleViewset, basename='role'),
router.register(r'permission', permissionView.PermissionViewset, basename='permission'),
router.register(r'patient', patientView.PatientViewSet, basename='patient'),
router.register(r'visit', visitView.VisitViewSet, basename='visit'),
router .register(r'symptom', SymptomViewSet, basename='symptom'),
router.register(r'medicinSymptom', MedicineSymptomViewSet, basename='medicineSymptom'),
router.register(r'medicine', MedicineViewSet, basename='medicineSuggestion'),
router.register(r'doctorProfile', DoctorProfileViewSet, basename='doctorProfile'),


# Create a schema view for drf-yasg
schema_view = get_schema_view(
    openapi.Info(
        title="Placeholder API",
        default_version='v1',
        description="Your API Description",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('',include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('changeMyPassword/', ChangeMyPasswordView.as_view(), name='changeMyPassword'),
    path('passwordReset/', PasswordResetRequestView.as_view(), name='passwordResetRequest'),
    # path('pass-reset/<str:temp_token>/', PasswordResetConfirmView.as_view(), name='pass-reset'),  # put it in security(auth) app's urls
    path('isSuperUser/', CheckUserType.as_view(), name='isSuperUser'),
    path('createUser/', createUserViews.CreateUserAPI.as_view(), name='create-user'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
