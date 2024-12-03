from django.db import models
from django.contrib.auth.models import User

# Profile model to extend user details
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='dependents')
    relationship = models.CharField(max_length=50)  # e.g., Father, Mother, Spouse, Child
    name = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    not_applicable = models.BooleanField(default=False)  # For marking as not applicable

    def __str__(self):
        return f"{self.relationship} - {self.name or 'Not Applicable'}"
