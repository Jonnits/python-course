from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    """
    View function for user login.
    """
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

