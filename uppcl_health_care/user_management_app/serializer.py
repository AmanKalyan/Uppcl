# user_management_app/serializers.py

from rest_framework import serializers
from .models import Employee, Dependent

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'unit_posted', 'sap_id', 'ppo_number', 'mobile_number', 'email_id', 'designation']

class DependentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependent
        fields = ['id', 'employee', 'name', 'age']
