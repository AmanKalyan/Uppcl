from django.db import models
from user_management_app.models import Employee, Dependent

class MedicalReimbursement(models.Model):
    TREATMENT_TYPE_CHOICES = [
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="reimbursements")
    patient = models.ForeignKey(Dependent, on_delete=models.SET_NULL, null=True, blank=True)
    treatment_type = models.CharField(max_length=10, choices=TREATMENT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reimbursement for {self.employee.name} - {self.treatment_type}"
    
class IndoorDetails(models.Model):
    reimbursement = models.OneToOneField(MedicalReimbursement, on_delete=models.CASCADE, related_name="indoor_details")
    ward_entitled = models.CharField(max_length=20, choices=[('General', 'General'), ('Semi Private', 'Semi Private'), ('Private', 'Private')], blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    treating_doctor = models.CharField(max_length=255, blank=True, null=True)
    admission_date = models.DateField(blank=True, null=True)
    discharge_date = models.DateField(blank=True, null=True)

    # Expense breakdown
    accommodation_general = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    accommodation_semi_private = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    accommodation_private = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    accommodation_icu = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    investigations = models.TextField(blank=True, null=True)
    procedures = models.TextField(blank=True, null=True)
    medicines_consumables = models.TextField(blank=True, null=True)
    implants = models.TextField(blank=True, null=True)
    other_charges = models.TextField(blank=True, null=True)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Indoor Details for {self.reimbursement}"

class OutdoorDetails(models.Model):
    reimbursement = models.OneToOneField(MedicalReimbursement, on_delete=models.CASCADE, related_name="outdoor_details")
    ward_entitled = models.CharField(max_length=20, choices=[('General', 'General'), ('Semi Private', 'Semi Private'), ('Private', 'Private')], blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    treating_doctor = models.CharField(max_length=255, blank=True, null=True)
    long_term_illness = models.TextField(blank=True, null=True)
    treatment_period_from = models.DateField(blank=True, null=True)
    treatment_period_to = models.DateField(blank=True, null=True)
    dialysis = models.BooleanField(default=False)
    chemotherapy = models.BooleanField(default=False)
    radiotherapy = models.BooleanField(default=False)
    emergency_treatment = models.BooleanField(default=False)
    diagnostic_tests = models.TextField(blank=True, null=True)
    hearing_aids_denture = models.BooleanField(default=False)
    anti_rabies_treatment = models.BooleanField(default=False)
    other_charges = models.TextField(blank=True, null=True)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Outdoor Details for {self.reimbursement}"
