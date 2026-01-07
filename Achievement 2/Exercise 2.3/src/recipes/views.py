from django.shortcuts import render

def recipes_home(request):
    """
    View function for the recipes home page.
    """
    return render(request, 'recipes/recipes_home.html')