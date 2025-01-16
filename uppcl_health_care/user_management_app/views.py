from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Employee, Dependent
from .forms import EmployeeForm, DependentFormSet, DependentForm
from django.urls import reverse

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        group = request.POST['group']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Optionally, store the group information in session or redirect to different views based on the group
            request.session['group'] = group  # Save selected group to session
            return redirect('user_management:reimbursement_selection')  # Redirect after successful login
        else:
            return render(request, 'user_management_app/login.html', {'error': 'Invalid credentials'})
    return render(request, 'user_management_app/login.html')

#user logout view
@login_required
def user_logout(request):
    logout(request) #log the user out
    return redirect('user_management:user_login')

def home(request):
    # Redirect to the login page when visiting the root URL
    return render(request, 'user_management_app/home.html')

def reimbursement_selection(request):
    if request.method == 'POST':
        reimbursement_type = request.POST.get('reimbursement_type')
        print(f"Reimbursement Type: {reimbursement_type}")  # Debugging
         # Redirect based on selected reimbursement type
        if reimbursement_type == 'medical_reimbursement':
            return redirect('medical_reimbursement:medical_reimbursement')
        elif reimbursement_type == 'medical_cashless':
            return redirect('medical_cashless:cashless_treatment')
        elif reimbursement_type == 'medical_advance':
            return redirect('medical_advance_treatment:medical_advance_form')
          # If no valid type is selected, re-render the form
        return render(request, 'user_management_app/reimbursement_selection.html', {
            'error_message': 'Please select a valid option.'
        })
    return render(request, 'user_management_app/reimbursement_selection.html')

def user_signup(request):
    if request.method == 'POST':
        print("POST data received:", request.POST)  # Debugging line
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        group = request.POST['group']  # Capture the group selection
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('user_management:user_signup')
        
        #create the new user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        
        # Optionally, store group information in the session or database
        request.session['group'] = group  # Save selected group to session
        
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('user_management:user_login')
    return render(request, 'user_management_app/signup.html')


def user_profile(request):
    try:
        employee = Employee.objects.get(user=request.user)
        dependents = Dependent.objects.filter(employee=employee)
    except Employee.DoesNotExist:
        return redirect('user_management:add_details')  # Redirect if no profile exists

    context = {
        'employee': employee,
        'dependents': dependents,
    }
    return render(request, 'user_management_app/profile.html', context)

# def add_details(request):
#     employee, created = Employee.objects.get_or_create(user=request.user)
#     dependent_instances = employee.dependents.all()
   

#     if request.method == 'POST':
#         employee_form = EmployeeForm(request.POST, instance=employee)
#         if employee_form.is_valid():
#             employee_form.save()
#             for dependent in dependent_instances:
#                 dependent_id = f"dependent_{dependent.id}"
#                 dependent.name = request.POST.get(f'name_{dependent_id}', dependent.name)
#                 dependent.age = request.POST.get(f'age_{dependent_id}', dependent.age)
#                 dependent.not_applicable = request.POST.get(f'not_applicable_{dependent_id}', 'off') == 'on'
#                 dependent.save()
#             if request.POST.get("add_child"):
#                 Dependent.objects.create(profile=profile, relationship="Child")
#             return redirect('user_profile')
#     else:
#         employee_form = EmployeeForm(instance=employee)
#     return render(request, 'user_management_app/add_details.html', {'employee_form': employee_form, 'dependent_instances': dependent_instances})

def add_details(request):
    # Get or create the employee instance
    employee, created = Employee.objects.get_or_create(user=request.user)

    # Handle fixed dependents
    fixed_dependents = {
        "Father": Dependent.objects.filter(employee=employee, relationship="Father").first(),
        "Mother": Dependent.objects.filter(employee=employee, relationship="Mother").first(),
        "Spouse": Dependent.objects.filter(employee=employee, relationship="Spouse").first(),
    }

    if request.method == "POST":
        # Handle POST data
        employee_form = EmployeeForm(request.POST, instance=employee)
        dependent_formset = DependentFormSet(
            request.POST, queryset=employee.dependents.filter(relationship="Child"), prefix="children"
        )
        fixed_forms = {
            relationship: DependentForm(request.POST, instance=fixed_dependents[relationship], prefix=relationship)
            for relationship in fixed_dependents
        }

        if (
            employee_form.is_valid()
            and all(form.is_valid() for form in fixed_forms.values())
            and dependent_formset.is_valid()
        ):
            employee_form.save()

            for relationship, form in fixed_forms.items():
                dependent = form.save(commit=False)
                dependent.employee = employee
                dependent.relationship = relationship
                dependent.save()

            children = dependent_formset.save(commit=False)
            for child in children:
                child.employee = employee
                child.relationship = "Child"
                child.save()
            dependent_formset.save_m2m()

            return redirect("user_management:user_profile")

    else:
        employee_form = EmployeeForm(instance=employee)
        dependent_formset = DependentFormSet(
            queryset=employee.dependents.filter(relationship="Child"), prefix="children"
        )
        fixed_forms = {
            relationship: DependentForm(instance=fixed_dependents[relationship], prefix=relationship)
            for relationship in fixed_dependents
        }

    empty_form = DependentForm(prefix="children-empty").as_p()

    return render(
        request,
        "user_management_app/add_details.html",
        {
            "employee_form": employee_form,
            "dependent_formset": dependent_formset,
            "fixed_forms": fixed_forms,
            "empty_form": empty_form,
        },
    )

def profile_management(request):
    # Form initialization
    EmployeeFormSet = formset_factory(EmployeeForm, extra=1)
    DependentFormSet = formset_factory(DependentForm, extra=0)

    if request.method == "POST":
        # Handle form submission
        employee_formset = EmployeeFormSet(request.POST, prefix="employee")
        dependent_formset = DependentFormSet(request.POST, prefix="dependent")

        if employee_formset.is_valid() and dependent_formset.is_valid():
            # Save all forms
            for form in employee_formset:
                form.save()
            for form in dependent_formset:
                form.save()
            return redirect('profile_success')
    else:
        # Initialize formsets
        employee_formset = EmployeeFormSet(prefix="employee")
        dependent_formset = DependentFormSet(prefix="dependent")
        empty_form = DependentFormSet(prefix="dependent").empty_form
        empty_form_html = empty_form.as_p().replace("\n", "")

    return render(
        request,
        "user_management_app/add_details.html",
        {
            "employee_formset": employee_formset,
            "dependent_formset": dependent_formset,
            "empty_form": empty_form_html,
        },
    )
