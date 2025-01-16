from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import MedicalReimbursement, IndoorDetails, OutdoorDetails
from user_management_app.models import Employee, Dependent
from .serializers import IndoorDetailsSerializer

# View: Medical Reimbursement Form
def medical_reimbursement(request):
    government_hospitals = [
        'Hospital A', 'Hospital B', 'Hospital C', 'Hospital D', 'Hospital E',
        'Hospital F', 'Hospital G', 'Hospital H', 'Hospital I', 'Hospital J', 'Others'
    ]
    empaneled_hospitals = [
        'Empaneled A', 'Empaneled B', 'Empaneled C', 'Empaneled D', 'Empaneled E',
        'Empaneled F', 'Empaneled G', 'Empaneled H', 'Empaneled I', 'Empaneled J'
    ]

    if request.method == 'POST':
        # Process form data
        treatment_type = request.POST.get("treatment_type")
        hospital_type = request.POST.get("hospital_type")
        government_hospital = request.POST.get("government_hospital")
        government_hospital_others = request.POST.get("government_hospital_others", "")
        empaneled_hospital = request.POST.get("empaneled_hospital")
        non_empaneled_hospital = request.POST.get("non_empaneled_hospital")
        income_tax_exempt = request.POST.get("income_tax_exempt")

        # Handle data processing or saving logic if needed

        # Redirect to patient selection after form submission
        return redirect("medical_reimbursement:patient_selection")

    # Render the form with hospital options
    context = {
        "government_hospitals": government_hospitals,
        "empaneled_hospitals": empaneled_hospitals,
    }
    return render(request, "medical_reimbursement_app/medical_reimbursement.html", context)


# View: Patient Selection Page
def patient_selection(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect("user_management:user_login")

    # Fetch the logged-in user's employee profile
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, "Employee details not found. Please contact the administrator.")
        return render(request, "medical_reimbursement_app/patient_selection.html", {"patients": []})

    # Fetch dependents for the employee
    dependents = employee.dependents.all()

    # Prepare patient data
    patients = [{"id": "self", "name": f"{employee.name} (Self)"}]  # Add self (employee) to list
    if dependents.exists():
        patients.extend(
            [{"id": dependent.id, "name": f"{dependent.name} ({dependent.relationship})"} for dependent in dependents]
        )

    if not patients:
        messages.error(request, "No dependent details available. Please update your profile.")
        return render(request, "medical_reimbursement_app/patient_selection.html", {"patients": []})

    # Handle POST Request
    if request.method == "POST":
        selected_patient = request.POST.get("patient")
        treatment_type = request.POST.get("treatment_type")

        if not selected_patient or not treatment_type:
            messages.error(request, "Please select both a patient and a treatment type.")
            return render(request, "medical_reimbursement_app/patient_selection.html", {"patients": patients})

        # Redirect to respective form based on treatment type
        if selected_patient == "self":
            patient = None  # Self representation
        else:
            try:
                patient = Dependent.objects.get(id=selected_patient)
            except Dependent.DoesNotExist:
                messages.error(request, "Invalid patient selection. Please try again.")
                return render(request, "medical_reimbursement_app/patient_selection.html", {"patients": patients})

        # Create a reimbursement record (save session ID for subsequent forms)
        reimbursement = MedicalReimbursement.objects.create(
            employee=employee,
            patient=patient,
            treatment_type=treatment_type
        )
        request.session["reimbursement_id"] = reimbursement.id

        # Redirect to the correct form
        if treatment_type == "Indoor":
            return redirect("medical_reimbursement:indoor_form")
        elif treatment_type == "Outdoor":
            return redirect("medical_reimbursement:outdoor_form")

    return render(request, "medical_reimbursement_app/patient_selection.html", {"patients": patients})

def indoor_form(request):
    if request.method == "POST":
        reimbursement_id = request.session.get("reimbursement_id")
        reimbursement = get_object_or_404(MedicalReimbursement, id=reimbursement_id)

        # Include reimbursement ID in the data
        data = request.POST.dict()
        data["reimbursement"] = reimbursement.id

        # Validate and save using the serializer
        serializer = IndoorDetailsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Indoor treatment details submitted successfully!")
            return redirect("medical_reimbursement:medical_reimbursement_form")
        else:
            # Display errors to the user
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

        return render(request, "medical_reimbursement_app/indoor_form.html", {
            "errors": serializer.errors,  # Pass errors to the template
        })

    elif request.method == "GET":
        # Render the form template for GET requests
        return render(request, "medical_reimbursement_app/indoor_form.html")

    # Return an appropriate HTTP response for unsupported methods
    return redirect("medical_reimbursement:medical_reimbursement_form")

def outdoor_form(request):
    if request.method == "POST":
        # Handle Outdoor form submission
        reimbursement_id = request.session.get("reimbursement_id")
        reimbursement = MedicalReimbursement.objects.get(id=reimbursement_id)

        OutdoorDetails.objects.create(
            reimbursement=reimbursement,
            ward_entitled=request.POST.get("ward_entitled"),
            diagnosis=request.POST.get("diagnosis"),
            treating_doctor=request.POST.get("treating_doctor"),
            long_term_illness=request.POST.get("long_term_illness"),
            treatment_period_from=request.POST.get("treatment_period_from"),
            treatment_period_to=request.POST.get("treatment_period_to"),
            dialysis=request.POST.get("dialysis") == "on",
            chemotherapy=request.POST.get("chemotherapy") == "on",
            radiotherapy=request.POST.get("radiotherapy") == "on",
            emergency_treatment=request.POST.get("emergency_treatment") == "on",
            diagnostic_tests=request.POST.get("diagnostic_tests"),
            hearing_aids_denture=request.POST.get("hearing_aids_denture") == "on",
            anti_rabies_treatment=request.POST.get("anti_rabies_treatment") == "on",
            other_charges=request.POST.get("other_charges"),
            total_expenses=request.POST.get("total_expenses"),
        )
        return redirect("medical_reimbursement:medical_reimbursement_form")

    return render(request, "medical_reimbursement_app/outdoor_form.html")

# this page will display all the filled data for verification.
def medical_reimbursement_form(request):
    reimbursement_id = request.session.get("reimbursement_id")
    reimbursement = MedicalReimbursement.objects.get(id=reimbursement_id)

    # Fetch case-specific details
    indoor_details = getattr(reimbursement, "indoor_details", None)
    outdoor_details = getattr(reimbursement, "outdoor_details", None)

    return render(request, "medical_reimbursement_app/medical_reimbursement_form.html", {
        "reimbursement": reimbursement,
        "indoor_details": indoor_details,
        "outdoor_details": outdoor_details,
    })