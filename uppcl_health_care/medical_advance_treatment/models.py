from django.db import models
from user_management_app.models import Employee, Dependent  # Import the related models

class MedicalAdvance(models.Model):
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name="medical_advances",
        help_text="Employee requesting medical advance."
    )
    patient = models.ForeignKey(
        Dependent, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="medical_advances",
        help_text="Patient for whom the medical advance is requested."
    )
    hospital_name = models.CharField(max_length=255)
    treating_doctor = models.CharField(max_length=255)
    diagnosis = models.CharField(max_length=255)
    treatment_type = models.CharField(
        max_length=20,
        choices=[("Conservative", "Conservative"), ("Surgical", "Surgical")],
    )
    procedure_cghs = models.CharField(max_length=255, null=True, blank=True)
    procedure_cghs_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    procedure_non_cghs = models.CharField(max_length=255, null=True, blank=True)
    procedure_non_cghs_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    implants_cghs = models.CharField(max_length=255, null=True, blank=True)
    implants_cghs_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    implants_non_cghs = models.CharField(max_length=255, null=True, blank=True)
    implants_non_cghs_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    other_consumables = models.CharField(max_length=255, null=True, blank=True)
    other_consumables_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Medical Advance for {self.employee.name} - {self.hospital_name}"
