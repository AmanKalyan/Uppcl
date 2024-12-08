from django.db import models
from django.contrib.auth.models import User

# Profile model to extend user details
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile")
    name = models.CharField(max_length=100)
    unit_posted = models.CharField(max_length=255)
    sap_id = models.CharField(max_length=50, unique=True)
    ppo_number = models.CharField(max_length=50, blank=True, null=True)
    mobile_number = models.CharField(max_length=15)
    email_id = models.EmailField()
    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

# Dependent model

class Dependent(models.Model):
    RELATIONSHIP_CHOICES = [
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Spouse', 'Spouse'),
        ('Child', 'Child'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="dependents",null = True, blank=True)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)

    class Meta:
        verbose_name = "Dependent"
        verbose_name_plural = "Dependents"

    def __str__(self):
        return f"{self.name} ({self.relationship})"
