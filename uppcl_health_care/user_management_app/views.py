from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Dependent
from .forms import ProfileForm, DependentForm


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        group = request.POST['group']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Optionally, store the group information in session or redirect to different views based on the group
            request.session['group'] = group  # Save selected group to session
            return redirect('reimbursement_selection')  # Redirect after successful login
        else:
            return render(request, 'user_management_app/login.html', {'error': 'Invalid credentials'})
    return render(request, 'user_management_app/login.html')

#user logout view
@login_required
def user_logout(request):
    logout(request) #log the user out
    return redirect('user_login')

def home(request):
    # Redirect to the login page when visiting the root URL
    return render(request, 'user_management_app/home.html')

def reimbursement_selection(request):
    if request.method == 'POST':
        reimbursement_type = request.POST.get('reimbursement_type')
        if reimbursement_type == 'medical_reimbursement':
            return redirect('medical_reimbursement:patient_selection')
        elif reimbursement_type == 'medical_cashless':
            return redirect('medical_cashless:cashless_treatment')
        elif reimbursement_type == 'medical_advance':
            return redirect('medical_advance:advance_treatment')
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
            return redirect('user_signup')
        
        #create the new user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        
        # Optionally, store group information in the session or database
        request.session['group'] = group  # Save selected group to session
        
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('user_login')
    return render(request, 'user_management_app/signup.html')


def user_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
        dependents = Dependent.objects.filter(profile=profile)
    except Profile.DoesNotExist:
        return redirect('add_details')  # Redirect if no profile exists

    context = {
        'profile': profile,
        'dependents': dependents,
    }
    return render(request, 'user_management_app/profile.html', context)
def add_details(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    dependent_instances = profile.dependents.all()
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            for dependent in dependent_instances:
                dependent_id = f"dependent_{dependent.id}"
                dependent.name = request.POST.get(f'name_{dependent_id}', dependent.name)
                dependent.age = request.POST.get(f'age_{dependent_id}', dependent.age)
                dependent.not_applicable = request.POST.get(f'not_applicable_{dependent_id}', 'off') == 'on'
                dependent.save()
            if request.POST.get("add_child"):
                Dependent.objects.create(profile=profile, relationship="Child")
            return redirect('user_profile')
    else:
        profile_form = ProfileForm(instance=profile)
    return render(request, 'user_management_app/add_details.html', {'profile_form': profile_form, 'dependent_instances': dependent_instances})




def profile_management(request):
    profile_form = ProfileForm()
    dependent_form = DependentForm()

    if request.method == 'POST':
        # Populate forms with submitted data
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        dependent_form = DependentForm(request.POST)

        if profile_form.is_valid() and dependent_form.is_valid():
            # Save the profile data
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()

            # Save the dependent data
            dependent = dependent_form.save(commit=False)
            dependent.profile = profile
            dependent.save()

            # Redirect to the profile page
            return redirect('user_profile')  # Replace with your profile page route

    return render(request, 'user_management_app/add_details.html', {
        'profile_form': profile_form,
        'dependent_form': dependent_form,
    })