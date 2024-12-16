from django.urls import path
from . import views

urlpatterns = [
    path('medical-reimbursement/', views.medical_reimbursement, name='medical_reimbursement'),
    path('', views.medical_reimbursement,name="medical_reimbursement"),
    path('patient-selection/', views.patient_selection, name='patient_selection'),
    ]
