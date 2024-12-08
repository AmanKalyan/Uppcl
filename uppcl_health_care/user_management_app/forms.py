# forms.py
from django import forms
from django.forms import modelformset_factory
from .models import Employee, Dependent

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'unit_posted', 'sap_id', 'ppo_number', 'mobile_number', 'email_id', 'designation']

class DependentForm(forms.ModelForm):
    class Meta:
        model = Dependent
        fields = ["name", "age"]


DependentFormSet = modelformset_factory(Dependent, form=DependentForm, extra=1)