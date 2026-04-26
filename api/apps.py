from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        import api.UserProfile
        import api.Patient.model
        import api.Visit.model
        import api.Symptom.model
        import api.Medicine.model
        import api.MedicineSymtom.model
        import api.DoctorProfile.model
        