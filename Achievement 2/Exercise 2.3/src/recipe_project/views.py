from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm
from users.models import UserProfile

def login_view(request):
    """
    View function for user login.
    """
    # Check if user is already logged in
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('recipes:recipes_list')
    
    error_message = None
    form = AuthenticationForm()
    
    # When user hits "login" button, then POST request is generated
    if request.method == 'POST':
        # Read the data sent by the form via POST request
        form = AuthenticationForm(data=request.POST)
        
        # Check if form is valid
        if form.is_valid():
            username = form.cleaned_data.get('username')  # Read username
            password = form.cleaned_data.get('password')   # Read password
            
            # Use Django authenticate function to validate the user
            user = authenticate(username=username, password=password)
            if user is not None:  # If user is authenticated
                # Then use pre-defined Django function to login
                login(request, user)
                return redirect('recipes:recipes_list')  # Send the user to recipes list page
        else:  # In case of error
            error_message = 'Oops.. something went wrong'
    
    # Prepare data to send from view to template
    context = {
        'form': form,  # Send the form data
        'error_message': error_message  # And the error_message
    }
    # Load the login page using "context" information
    return render(request, 'auth/login.html', context)

def logout_view(request):
    """
    View function for user logout.
    """
    logout(request)  # Use pre-defined Django function to logout
    return redirect('logout_success')  # After logging out go to success page

def logout_success(request):
    """
    View function to display logout success page.
    """
    return render(request, 'auth/success.html')

def register_view(request):
    """
    View function for user registration.
    """
    error_message = None
    form = UserRegistrationForm()
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after registration
            login(request, user)
            return redirect('recipes:recipes_list')
        else:
            error_message = 'Please correct the errors below.'
    
    context = {
        'form': form,
        'error_message': error_message
    }
    return render(request, 'auth/register.html', context)

@login_required
def delete_profile(request):
    """
    Delete user profile with confirmation.
    """
    if request.method == 'POST':
        # User confirmed deletion
        user = request.user
        user.delete()  # This will cascade delete UserProfile
        messages.success(request, 'Your profile has been deleted.')
        return redirect('recipes:recipes_home')
    
    # Show confirmation page
    return render(request, 'auth/delete_profile_confirm.html')

