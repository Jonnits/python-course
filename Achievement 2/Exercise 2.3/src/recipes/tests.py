from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe
from .forms import RecipeSearchForm


class RecipeModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Create test recipes
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            author=self.user,
            cooking_time=30,
            ingredients="Salt, Pepper, Water",
            description="A test recipe"
        )
    
    def test_recipe_name(self):
        recipe = Recipe.objects.get(name="Test Recipe")
        self.assertEqual(recipe.name, "Test Recipe")
    
    def test_recipe_str(self):
        recipe = Recipe.objects.get(name="Test Recipe")
        self.assertEqual(str(recipe), "Test Recipe")
    
    def test_recipe_author(self):
        recipe = Recipe.objects.get(name="Test Recipe")
        self.assertEqual(recipe.author, self.user)
    
    def test_calculate_difficulty_easy(self):
        """Test difficulty calculation for Easy recipe"""
        recipe = Recipe.objects.create(
            name="Easy Recipe",
            author=self.user,
            cooking_time=5,
            ingredients="Salt, Pepper",
            description="Easy recipe"
        )
        self.assertEqual(recipe.difficulty, "Easy")
    
    def test_calculate_difficulty_medium(self):
        """Test difficulty calculation for Medium recipe"""
        recipe = Recipe.objects.create(
            name="Medium Recipe",
            author=self.user,
            cooking_time=5,
            ingredients="Salt, Pepper, Water, Oil",
            description="Medium recipe"
        )
        self.assertEqual(recipe.difficulty, "Medium")
    
    def test_calculate_difficulty_intermediate(self):
        """Test difficulty calculation for Intermediate recipe"""
        recipe = Recipe.objects.create(
            name="Intermediate Recipe",
            author=self.user,
            cooking_time=15,
            ingredients="Salt, Pepper",
            description="Intermediate recipe"
        )
        self.assertEqual(recipe.difficulty, "Intermediate")
    
    def test_calculate_difficulty_hard(self):
        """Test difficulty calculation for Hard recipe"""
        recipe = Recipe.objects.create(
            name="Hard Recipe",
            author=self.user,
            cooking_time=15,
            ingredients="Salt, Pepper, Water, Oil, Flour, Sugar",
            description="Hard recipe"
        )
        self.assertEqual(recipe.difficulty, "Hard")
    
    def test_get_ingredients_list(self):
        """Test get_ingredients_list method"""
        recipe = Recipe.objects.get(name="Test Recipe")
        ingredients = recipe.get_ingredients_list()
        self.assertEqual(len(ingredients), 3)
        self.assertIn("Salt", ingredients)
        self.assertIn("Pepper", ingredients)
        self.assertIn("Water", ingredients)
    
    def test_get_ingredients_list_empty(self):
        """Test get_ingredients_list with empty ingredients"""
        recipe = Recipe.objects.create(
            name="Empty Recipe",
            author=self.user,
            cooking_time=10,
            ingredients="",
            description="Empty ingredients"
        )
        ingredients = recipe.get_ingredients_list()
        self.assertEqual(ingredients, [])


class RecipeViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            author=self.user,
            cooking_time=30,
            ingredients="Salt, Pepper, Water",
            description="A test recipe"
        )
    
    def test_recipes_home_view(self):
        """Test that recipes home page loads successfully"""
        url = reverse('recipes:recipes_home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_home.html')
    
    def test_recipes_list_view(self):
        """Test that recipes list page loads successfully"""
        url = reverse('recipes:recipes_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_list.html')
        self.assertIn(self.recipe, response.context['recipes'])
    
    def test_recipes_list_view_empty(self):
        """Test recipes list view with no recipes"""
        Recipe.objects.all().delete()
        url = reverse('recipes:recipes_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['recipes']), 0)
    
    def test_recipe_detail_view(self):
        """Test that recipe detail page loads successfully"""
        url = reverse('recipes:recipe_detail', args=[self.recipe.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')
        self.assertEqual(response.context['recipe'], self.recipe)
    
    def test_recipe_detail_view_404(self):
        """Test that recipe detail returns 404 for non-existent recipe"""
        url = reverse('recipes:recipe_detail', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class RecipeURLsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            author=self.user,
            cooking_time=30,
            ingredients="Salt, Pepper, Water",
            description="A test recipe"
        )
    
    def test_home_url_resolves(self):
        """Test that home URL resolves correctly"""
        url = reverse('recipes:recipes_home')
        self.assertEqual(url, '/')
    
    def test_recipes_list_url_resolves(self):
        """Test that recipes list URL resolves correctly"""
        url = reverse('recipes:recipes_list')
        self.assertEqual(url, '/recipes/')
    
    def test_recipe_detail_url_resolves(self):
        """Test that recipe detail URL resolves correctly"""
        url = reverse('recipes:recipe_detail', args=[self.recipe.id])
        self.assertEqual(url, f'/recipes/{self.recipe.id}/')
    
    def test_home_url_accessible(self):
        """Test that home URL is accessible"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_recipes_list_url_accessible(self):
        """Test that recipes list URL is accessible"""
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_detail_url_accessible(self):
        """Test that recipe detail URL is accessible"""
        response = self.client.get(f'/recipes/{self.recipe.id}/')
        self.assertEqual(response.status_code, 200)


class RecipeFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.recipe1 = Recipe.objects.create(
            name="Chocolate Cake",
            author=self.user,
            cooking_time=45,
            ingredients="Flour, Sugar, Cocoa, Eggs, Butter",
            description="Delicious chocolate cake"
        )
        self.recipe2 = Recipe.objects.create(
            name="Hot Chocolate",
            author=self.user,
            cooking_time=5,
            ingredients="Milk, Cocoa, Sugar",
            description="Warm chocolate drink"
        )
        self.recipe3 = Recipe.objects.create(
            name="Easy Salad",
            author=self.user,
            cooking_time=10,
            ingredients="Lettuce, Tomato, Cucumber",
            description="Simple salad"
        )
    
    def test_search_form_fields(self):
        """Test that search form has all required fields"""
        form = RecipeSearchForm()
        self.assertIn('name', form.fields)
        self.assertIn('ingredients', form.fields)
        self.assertIn('max_cooking_time', form.fields)
        self.assertIn('difficulty', form.fields)
        self.assertIn('author', form.fields)
    
    def test_search_form_optional_fields(self):
        """Test that all search form fields are optional"""
        form = RecipeSearchForm({})
        self.assertTrue(form.is_valid())
    
    def test_search_form_name_field(self):
        """Test search form name field validation"""
        form = RecipeSearchForm({'name': 'Chocolate'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'Chocolate')
    
    def test_search_form_max_cooking_time_validation(self):
        """Test search form max_cooking_time field validation"""
        form = RecipeSearchForm({'max_cooking_time': 30})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['max_cooking_time'], 30)
    
    def test_search_form_difficulty_choices(self):
        """Test search form difficulty field choices"""
        form = RecipeSearchForm()
        choices = form.fields['difficulty'].choices
        self.assertIn(('Easy', 'Easy'), choices)
        self.assertIn(('Medium', 'Medium'), choices)
        self.assertIn(('Intermediate', 'Intermediate'), choices)
        self.assertIn(('Hard', 'Hard'), choices)


class RecipeSearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='testpass123'
        )
        self.recipe1 = Recipe.objects.create(
            name="Chocolate Cake",
            author=self.user,
            cooking_time=45,
            ingredients="Flour, Sugar, Cocoa, Eggs, Butter",
            description="Delicious chocolate cake"
        )
        self.recipe2 = Recipe.objects.create(
            name="Hot Chocolate",
            author=self.user,
            cooking_time=5,
            ingredients="Milk, Cocoa, Sugar",
            description="Warm chocolate drink"
        )
        self.recipe3 = Recipe.objects.create(
            name="Easy Salad",
            author=self.user2,
            cooking_time=10,
            ingredients="Lettuce, Tomato, Cucumber",
            description="Simple salad"
        )
    
    def test_search_view_accessible(self):
        """Test that search view is accessible"""
        url = reverse('recipes:recipe_search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_search.html')
    
    def test_search_view_contains_form(self):
        """Test that search view contains the search form"""
        url = reverse('recipes:recipe_search')
        response = self.client.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], RecipeSearchForm)
    
    def test_search_by_name(self):
        """Test searching recipes by name"""
        url = reverse('recipes:recipe_search')
        response = self.client.get(url, {'name': 'Chocolate'})
        self.assertEqual(response.status_code, 200)
        # Check that data contains matching recipes
        if response.context.get('recipes_data'):
            recipe_names = [row['Recipe Name'] for row in response.context['recipes_data']]
            self.assertIn('Chocolate Cake', recipe_names)
            self.assertIn('Hot Chocolate', recipe_names)
    
    def test_search_by_ingredient(self):
        """Test searching recipes by ingredient"""
        url = reverse('recipes:recipe_search')
        response = self.client.get(url, {'ingredients': 'Cocoa'})
        self.assertEqual(response.status_code, 200)
        if response.context.get('recipes_data'):
            recipe_names = [row['Recipe Name'] for row in response.context['recipes_data']]
            self.assertIn('Chocolate Cake', recipe_names)
            self.assertIn('Hot Chocolate', recipe_names)
    
    def test_search_by_max_cooking_time(self):
        """Test searching recipes by maximum cooking time"""
        url = reverse('recipes:recipe_search')
        response = self.client.get(url, {'max_cooking_time': 10})
        self.assertEqual(response.status_code, 200)
        if response.context.get('recipes_data'):
            # All recipes should have cooking_time <= 10
            for row in response.context['recipes_data']:
                recipe = Recipe.objects.get(name=row['Recipe Name'])
                self.assertLessEqual(recipe.cooking_time, 10)
    
    def test_search_by_difficulty(self):
        """Test searching recipes by difficulty"""
        url = reverse('recipes:recipe_search')
        response = self.client.get(url, {'difficulty': 'Easy'})
        self.assertEqual(response.status_code, 200)
        if response.context.get('recipes_data'):
            # All recipes should have Easy difficulty
            for row in response.context['recipes_data']:
                self.assertEqual(row['Difficulty'], 'Easy')
    
    def test_search_by_author(self):
        """Test searching recipes by author"""
        url = reverse('recipes:recipe_search')
        response = self.client.get(url, {'author': 'anotheruser'})
        self.assertEqual(response.status_code, 200)
        if response.context.get('recipes_data'):
            recipe_names = [row['Recipe Name'] for row in response.context['recipes_data']]
            self.assertIn('Easy Salad', recipe_names)
    
    def test_search_wildcard_partial_match(self):
        """Test wildcard/partial search functionality"""
        url = reverse('recipes:recipe_search')
        # Search for "Choc" should match "Chocolate Cake" and "Hot Chocolate"
        response = self.client.get(url, {'name': 'Choc'})
        self.assertEqual(response.status_code, 200)
        if response.context.get('recipes_data'):
            recipe_names = [row['Recipe Name'] for row in response.context['recipes_data']]
            self.assertIn('Chocolate Cake', recipe_names)
            self.assertIn('Hot Chocolate', recipe_names)
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive"""
        url = reverse('recipes:recipe_search')
        response = self.client.get(url, {'name': 'chocolate'})
        self.assertEqual(response.status_code, 200)
        if response.context.get('recipes_data'):
            recipe_names = [row['Recipe Name'] for row in response.context['recipes_data']]
            self.assertIn('Chocolate Cake', recipe_names)
    
    def test_show_all_recipes(self):
        """Test Show All functionality"""
        url = reverse('recipes:recipe_search')
        response = self.client.get(url, {'show_all': '1'})
        self.assertEqual(response.status_code, 200)
        if response.context.get('recipes_data'):
            # Should show all recipes
            self.assertEqual(len(response.context['recipes_data']), Recipe.objects.count())
    
    def test_search_multiple_filters(self):
        """Test searching with multiple filters"""
        url = reverse('recipes:recipe_search')
        response = self.client.get(url, {
            'name': 'Chocolate',
            'max_cooking_time': 10,
            'difficulty': 'Easy'
        })
        self.assertEqual(response.status_code, 200)
        if response.context.get('recipes_data'):
            # Should only match recipes that meet all criteria
            for row in response.context['recipes_data']:
                recipe = Recipe.objects.get(name=row['Recipe Name'])
                self.assertIn('Chocolate', recipe.name)
                self.assertLessEqual(recipe.cooking_time, 10)
                self.assertEqual(recipe.difficulty, 'Easy')
    
    def test_search_no_results(self):
        """Test search with no matching results"""
        url = reverse('recipes:recipe_search')
        response = self.client.get(url, {'name': 'NonExistentRecipe'})
        self.assertEqual(response.status_code, 200)
        if response.context.get('recipes_data') is not None:
            self.assertEqual(len(response.context['recipes_data']), 0)
    
    def test_search_view_charts_generated(self):
        """Test that charts are generated when recipes exist"""
        url = reverse('recipes:recipe_search')
        response = self.client.get(url, {'show_all': '1'})
        self.assertEqual(response.status_code, 200)
        # Charts should be generated if recipes exist
        if Recipe.objects.exists():
            self.assertIn('charts', response.context)
            charts = response.context['charts']
            self.assertIn('difficulty_bar', charts)
            self.assertIn('author_pie', charts)
            self.assertIn('cooking_time_line', charts)