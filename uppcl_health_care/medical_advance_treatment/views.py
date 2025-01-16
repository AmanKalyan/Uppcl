from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MedicalAdvance, Employee, Dependent
from .serializers import MedicalAdvanceSerializer

class MedicalAdvanceView(APIView):
    def get(self, request):
        try:
            # Fetch the logged-in user's employee profile
            employee = request.user.employee_profile
        except Employee.DoesNotExist:
            # Handle case where employee details are missing
            return render(request, "medical_advance_treatment/medical_advance_form.html", {
                "error_message": "Employee details not found. Please contact the administrator."
            })

        # Gather dependents and construct patient options
        dependents = employee.dependents.all()
        patients = [{"id": "self", "name": f"{employee.name} (Self)"}]
        patients.extend([{"id": dependent.id, "name": f"{dependent.name} ({dependent.relationship})"} for dependent in dependents])

        # Render the form template with employee and patient details
        return render(request, "medical_advance_treatment/medical_advance_form.html", {
            "employee": employee,
            "patients": patients,
        })

    def post(self, request):
        try:
            # Fetch the logged-in user's employee profile
            employee = request.user.employee_profile
        except Employee.DoesNotExist:
            # Return a 404 error response if employee details are missing
            return Response({"error": "Employee details not found."}, status=status.HTTP_404_NOT_FOUND)

        # Prepare data for the serializer
        data = request.data.copy()
        data["employee"] = employee.id

        if data.get("patient") == "self":
            data["patient"] = None  # Set to None if "Self" is selected

        # Validate and save the form data using the serializer
        serializer = MedicalAdvanceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # Redirect to success page after form submission
            return redirect("medical_advance_treatment:medical_advance_success", pk=serializer.instance.id)
        else:
            # Render the form with validation errors
            dependents = employee.dependents.all()
            patients = [{"id": "self", "name": f"{employee.name} (Self)"}]
            patients.extend([{"id": dependent.id, "name": f"{dependent.name} ({dependent.relationship})"} for dependent in dependents])

            return render(request, "medical_advance_treatment/medical_advance_form.html", {
                "errors": serializer.errors,
                "employee": employee,
                "patients": patients,
            })