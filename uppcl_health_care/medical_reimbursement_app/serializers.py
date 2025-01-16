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
        """
        Validate that total expenses is a positive decimal number.
        """
        if value is None:
            raise serializers.ValidationError("Total expenses cannot be empty.")
        if value < 0:
            raise serializers.ValidationError("Total expenses must be a positive value.")
        return value

    def validate(self, data):
        """
        Perform custom validation for related fields.
        """
        admission_date = data.get("admission_date")
        discharge_date = data.get("discharge_date")

        if admission_date and discharge_date and admission_date > discharge_date:
            raise serializers.ValidationError(
                {"discharge_date": "Discharge date cannot be earlier than admission date."}
            )

        # Check that at least one accommodation field is filled
        accommodation_fields = [
            "accommodation_general",
            "accommodation_semi_private",
            "accommodation_private",
            "accommodation_icu",
        ]
        if not any(data.get(field) for field in accommodation_fields):
            raise serializers.ValidationError(
                {"accommodation": "At least one accommodation field must be filled."}
            )

        return data
