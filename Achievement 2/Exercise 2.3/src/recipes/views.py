from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Count
from django.contrib import messages
from .models import Recipe
from .forms import RecipeSearchForm, RecipeForm
from users.models import UserProfile
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import base64
from io import BytesIO

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
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    is_favorited = recipe in user_profile.favorited_recipes.all()
    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'is_favorited': is_favorited
    })

@login_required
def toggle_favorite(request, recipe_id):
    """
    Toggle favorite status for a recipe.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if recipe in user_profile.favorited_recipes.all():
        user_profile.favorited_recipes.remove(recipe)
        messages.success(request, f'Removed {recipe.name} from favorites.')
    else:
        user_profile.favorited_recipes.add(recipe)
        messages.success(request, f'Added {recipe.name} to favorites.')
    
    return redirect('recipes:recipe_detail', recipe_id=recipe_id)

@login_required
def user_favorites(request):
    """
    Display user's favorite recipes.
    """
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    favorites = user_profile.favorited_recipes.all().order_by('name')
    return render(request, 'recipes/user_favorites.html', {
        'favorites': favorites,
        'user_profile': user_profile
    })

@login_required
def add_recipe(request):
    """
    View function for adding a new recipe.
    """
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, f'Recipe "{recipe.name}" has been added successfully!')
            return redirect('recipes:recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    
    return render(request, 'recipes/add_recipe.html', {'form': form})

def recipe_search(request):
    """
    View function for searching recipes with filters.
    Converts QuerySet to pandas DataFrame and displays results with visualizations.
    """
    form = RecipeSearchForm(request.GET or None)
    recipes = Recipe.objects.all()
    df = None
    charts = {}
    recipes_data = None
    columns = []
    
    # Check if "Show All" button was clicked
    show_all = request.GET.get('show_all', False)
    
    if show_all or (form.is_valid() and any(form.cleaned_data.values())):
        # Apply filters
        if form.is_valid():
            name = form.cleaned_data.get('name')
            ingredients = form.cleaned_data.get('ingredients')
            max_cooking_time = form.cleaned_data.get('max_cooking_time')
            difficulty = form.cleaned_data.get('difficulty')
            author = form.cleaned_data.get('author')
            
            # Build query with filters
            if name:
                recipes = recipes.filter(name__icontains=name)
            
            if ingredients:
                recipes = recipes.filter(ingredients__icontains=ingredients)
            
            if max_cooking_time:
                recipes = recipes.filter(cooking_time__lte=max_cooking_time)
            
            if difficulty:
                recipes = recipes.filter(difficulty=difficulty)
            
            if author:
                recipes = recipes.filter(author__username__icontains=author)
        
        # Order results
        recipes = recipes.order_by('name')
        
        # Convert QuerySet to pandas DataFrame
        if recipes.exists():
            data = []
            for recipe in recipes:
                ingredients_list = recipe.get_ingredients_list()
                ingredients_preview = ', '.join(ingredients_list[:3])
                if len(ingredients_list) > 3:
                    ingredients_preview += f' (+{len(ingredients_list) - 3} more)'
                
                data.append({
                    'Recipe Name': recipe.name,
                    'Author': recipe.author.username,
                    'Cooking Time (min)': recipe.cooking_time,
                    'Difficulty': recipe.difficulty,
                    'Ingredients': ingredients_preview,
                    'Recipe ID': recipe.id,  # For creating links
                })
            
            df = pd.DataFrame(data)
            # Convert DataFrame to list of dictionaries for template
            recipes_data = df.to_dict('records')
            # Get column names for table header
            columns = [col for col in df.columns if col != 'Recipe ID']
        else:
            recipes_data = []
            columns = []
        
        # Generate visualizations
        charts = generate_charts()
    
    context = {
        'form': form,
        'recipes_data': recipes_data,
        'recipes_columns': columns,
        'recipes_count': recipes.count() if recipes else 0,
        'charts': charts,
        'show_all': show_all,
    }
    
    return render(request, 'recipes/recipe_search.html', context)

def generate_charts():
    """
    Generate bar, pie, and line charts for recipe data visualization.
    Returns a dictionary with base64-encoded chart images.
    """
    charts = {}
    
    # Get all recipes for visualization
    all_recipes = Recipe.objects.all()
    
    if not all_recipes.exists():
        return charts
    
    # Chart 1: Bar Chart - Recipes by Difficulty Level
    difficulty_counts = all_recipes.values('difficulty').annotate(count=Count('id')).order_by('difficulty')
    difficulties = [item['difficulty'] for item in difficulty_counts]
    counts = [item['count'] for item in difficulty_counts]
    
    plt.figure(figsize=(10, 6))
    plt.bar(difficulties, counts, color=['#4CAF50', '#2196F3', '#FF9800', '#F44336'])
    plt.xlabel('Difficulty Level', fontsize=12)
    plt.ylabel('Number of Recipes', fontsize=12)
    plt.title('Recipes by Difficulty Level', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart1_base64 = base64.b64encode(buffer.read()).decode()
    plt.close()
    charts['difficulty_bar'] = chart1_base64
    
    # Chart 2: Pie Chart - Recipes by Author
    author_counts = all_recipes.values('author__username').annotate(count=Count('id')).order_by('-count')
    authors = [item['author__username'] for item in author_counts[:10]]  # Top 10 authors
    author_recipe_counts = [item['count'] for item in author_counts[:10]]
    
    # If more than 10 authors, group the rest as "Others"
    if author_counts.count() > 10:
        others_count = sum(item['count'] for item in author_counts[10:])
        authors.append('Others')
        author_recipe_counts.append(others_count)
    
    plt.figure(figsize=(10, 8))
    plt.pie(author_recipe_counts, labels=authors, autopct='%1.1f%%', startangle=90)
    plt.title('Recipes by Author', fontsize=14, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart2_base64 = base64.b64encode(buffer.read()).decode()
    plt.close()
    charts['author_pie'] = chart2_base64
    
    # Chart 3: Line Chart - Average Cooking Time by Difficulty
    avg_cooking_time = all_recipes.values('difficulty').annotate(
        avg_time=Avg('cooking_time')
    ).order_by('difficulty')
    
    difficulties_line = [item['difficulty'] for item in avg_cooking_time]
    avg_times = [item['avg_time'] for item in avg_cooking_time]
    
    plt.figure(figsize=(10, 6))
    plt.plot(difficulties_line, avg_times, marker='o', linewidth=2, markersize=8, color='#9C27B0')
    plt.xlabel('Difficulty Level', fontsize=12)
    plt.ylabel('Average Cooking Time (minutes)', fontsize=12)
    plt.title('Average Cooking Time by Difficulty Level', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart3_base64 = base64.b64encode(buffer.read()).decode()
    plt.close()
    charts['cooking_time_line'] = chart3_base64
    
    return charts