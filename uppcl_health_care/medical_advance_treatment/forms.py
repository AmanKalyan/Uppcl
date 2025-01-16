from django import forms
from .models import MedicalAdvance


class MedicalAdvanceForm(forms.ModelForm):
    class Meta:
        model = MedicalAdvance
        fields = "__all__"

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get("mobile_number")
        if not mobile_number.isdigit() or len(mobile_number) != 10:
            raise forms.ValidationError("Mobile number must be a 10-digit numeric value.")
        return mobile_number
