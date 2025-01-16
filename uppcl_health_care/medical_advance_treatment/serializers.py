from rest_framework import serializers
from medical_advance_treatment.models import MedicalAdvance

class MedicalAdvanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalAdvance
        fields = "__all__"

    def validate_mobile_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Mobile number must be a 10-digit numeric value.")
        return value

    def validate_total_cost(self, value):
        if value < 0:
            raise serializers.ValidationError("Total cost cannot be negative.")
        return value
