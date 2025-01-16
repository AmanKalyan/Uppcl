from rest_framework import serializers
from .models import IndoorDetails

class IndoorDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndoorDetails
        fields = [
            "ward_entitled",
            "diagnosis",
            "treating_doctor",
            "admission_date",
            "discharge_date",
            "accommodation_general",
            "accommodation_semi_private",
            "accommodation_private",
            "accommodation_icu",
            "investigations",
            "procedures",
            "medicines_consumables",
            "implants",
            "other_charges",
            "total_expenses",
        ]

    def validate_total_expenses(self, value):
        if value is None or value < 0:
            raise serializers.ValidationError("Total expenses must be a positive value.")
        return value

    def validate(self, data):
        admission_date = data.get("admission_date")
        discharge_date = data.get("discharge_date")
        if admission_date and discharge_date and admission_date > discharge_date:
            raise serializers.ValidationError(
                {"discharge_date": "Discharge date cannot be earlier than admission date."}
            )
        return data
