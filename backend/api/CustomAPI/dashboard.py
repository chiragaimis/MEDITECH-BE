from rest_framework.views import APIView
from rest_framework.response import Response
from collections import Counter

from api.Patient.model import Patient
from api.Visit.model import Visit
from api.Medicine.model import Medicine


class DashboardView(APIView):
    def get(self, request):
        visits = Visit.objects.select_related("patient").order_by("-visit_date")[:10]
        all_medicines = Visit.objects.values_list("medicines", flat=True)
        counter = Counter(med for meds in all_medicines for med in meds)

        return Response({
            "stats": {
                "total_patients": Patient.objects.count(),
                "total_visits": Visit.objects.count(),
                "total_medicines": Medicine.objects.count(),
            },
            "recent_visits": [
                {
                    "visit_id": str(v.id),
                    "patient_name": v.patient.name,
                    "patient_id": v.patient.patient_id,
                    "visit_date": v.visit_date,
                    "diagnosis": v.diagnosis,
                    "symptoms": v.symptoms,
                }
                for v in visits
            ],
            "top_medicines": [
                {"medicine": name, "count": count}
                for name, count in counter.most_common(10)
            ],
        })
