from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages

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
        return redirect("patient_selection")

    # Render the form with hospital options
    context = {
        "government_hospitals": government_hospitals,
        "empaneled_hospitals": empaneled_hospitals,
    }
    return render(request, "medical_reimbursement_app/medical_reimbursement.html", context)


# View: Patient Selection Page
def patient_selection(request):
    dependents = [
        {"id": 1, "name": "John Doe", "relationship": "Self"},
        {"id": 2, "name": "Jane Doe", "relationship": "Spouse"},
        {"id": 3, "name": "Jack Doe", "relationship": "Son"},
    ]

    if request.method == 'POST':
        # Handle patient selection and file uploads
        selected_patient = request.POST.get("patient")
        document_a = request.FILES.get("document_a")
        # document_b = request.FILES.get("document_b")
        # document_c = request.FILES.get("document_c")
        # document_d = request.FILES.get("document_d")
        # document_e = request.FILES.get("document_e")

        # Save files or process data as required
        print(f"Selected Patient: {selected_patient}")

        return redirect("success_page")  # Replace with an actual success page or next step

    return render(request, "medical_reimbursement_app/patient_selection.html", {"dependents": dependents})
