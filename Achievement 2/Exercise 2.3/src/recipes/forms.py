from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    """Form for adding/editing recipes"""
    
    class Meta:
        model = Recipe
        fields = ['name', 'cooking_time', 'ingredients', 'description', 'pic']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Recipe name...'
            }),
            'cooking_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cooking time in minutes',
                'min': 1
            }),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ingredients separated by commas (e.g., Salt, Pepper, Water)',
                'rows': 4
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Recipe description...',
                'rows': 6
            }),
            'pic': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'name': 'Recipe Name',
            'cooking_time': 'Cooking Time (minutes)',
            'ingredients': 'Ingredients',
            'description': 'Description',
            'pic': 'Recipe Image (optional)',
        }

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

