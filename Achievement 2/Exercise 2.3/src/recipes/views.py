from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Recipe

def recipes_home(request):
    """
    View function for the recipes home page.
    """
    return render(request, 'recipes/recipes_home.html')

def recipes_list(request):
    """
    View function to display all recipes in a list.
    """
    recipes = Recipe.objects.all().order_by('name')
    return render(request, 'recipes/recipes_list.html', {'recipes': recipes})

@login_required
def recipe_detail(request, recipe_id):
    """
    View function to display a single recipe's details.
    Protected view - requires user to be logged in.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})