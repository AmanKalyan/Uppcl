from django.urls import path
from . import views

app_name = "medical_reimbursement"

urlpatterns = [
    # path('medical-reimbursement/', views.medical_reimbursement, name='medical_reimbursement'),
    path('', views.medical_reimbursement,name="medical_reimbursement"),
    path('patient-selection/', views.patient_selection, name='patient_selection'),
    path('indoor-form/', views.indoor_form, name="indoor_form"),
    path('outdoor-form/', views.outdoor_form, name="outdoor_form"),
    path('medical-reimbursement-form/', views.medical_reimbursement_form, name="medical_reimbursement_form"),
    ]
