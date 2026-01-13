from django import forms
from .models import Recipe

class RecipeSearchForm(forms.Form):
    """Form for searching recipes"""
    
    DIFFICULTY_CHOICES = [
        ('', 'All Difficulties'),
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Intermediate', 'Intermediate'),
        ('Hard', 'Hard'),
    ]
    
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by recipe name...'
        }),
        label='Recipe Name'
    )
    
    ingredients = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by ingredient...'
        }),
        label='Ingredient'
    )
    
    max_cooking_time = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Maximum cooking time (minutes)',
            'min': 1
        }),
        label='Max Cooking Time (minutes)'
    )
    
    difficulty = forms.ChoiceField(
        required=False,
        choices=DIFFICULTY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Difficulty Level'
    )
    
    author = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by author username...'
        }),
        label='Author'
    )

