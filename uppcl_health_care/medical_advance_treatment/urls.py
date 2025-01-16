from django.urls import path
from . import views 
from medical_advance_treatment.views import MedicalAdvanceView

app_name = "medical_advance_treatment"

urlpatterns = [
    path("form/", MedicalAdvanceView.as_view(), name="medical_advance_form"),
    path("success/<int:pk>/", lambda request, pk: render(request, "medical_advance_treatment/success.html"), name="medical_advance_success"),
]
