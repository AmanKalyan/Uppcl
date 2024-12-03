from django import forms
from .models import Profile, Dependent

# Form for updating user profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['unit_posted', 'sap_id', 'ppo_number', 'mobile_number', 'email_id', 'designation']

# Form for updating dependent details
class DependentForm(forms.ModelForm):
    class Meta:
        model = Dependent
        fields = ['relationship', 'name', 'age', 'not_applicable']
