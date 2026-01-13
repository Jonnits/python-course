from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from users.models import UserProfile
import re

class UserRegistrationForm(forms.Form):
    """Custom registration form with specific validation requirements"""
    
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a unique username'
        }),
        label='Username'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        }),
        label='Email Address'
    )
    
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '8-16 characters, 1 number, 1 uppercase'
        }),
        label='Password',
        help_text='Password must be 8-16 characters long and include at least 1 number and 1 uppercase letter.'
    )
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        }),
        label='Confirm Password'
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('A user with this username already exists.')
        return username
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if not password:
            return password
        
        # Check length
        if len(password) < 8 or len(password) > 16:
            raise ValidationError('Password must be between 8 and 16 characters long.')
        
        # Check for at least one number
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one number.')
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match.')
        
        return cleaned_data
    
    def save(self):
        """Create and return a new user with profile"""
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Create UserProfile
        UserProfile.objects.create(
            user=user,
            name=username,  # Use username as default name
            email_address=email
        )
        
        return user

