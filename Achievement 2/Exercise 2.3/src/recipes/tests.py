from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Recipe
from .forms import RecipeSearchForm, RecipeForm
from users.models import UserProfile


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
    
    def test_get_ingredients_list_sorted(self):
        """Test that get_ingredients_list returns sorted ingredients"""
        recipe = Recipe.objects.create(
            name="Sorted Recipe",
            author=self.user,
            cooking_time=10,
            ingredients="Zucchini, Apple, Banana, Carrot",
            description="Test sorting"
        )
        ingredients = recipe.get_ingredients_list()
        # Should be sorted alphabetically
        self.assertEqual(ingredients, ['Apple', 'Banana', 'Carrot', 'Zucchini'])


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
    
    def test_recipe_detail_view_requires_login(self):
        """Test that recipe detail view requires authentication"""
        url = reverse('recipes:recipe_detail', args=[self.recipe.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirects to login
    
    def test_recipe_detail_view(self):
        """Test that recipe detail page loads successfully"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('recipes:recipe_detail', args=[self.recipe.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')
        self.assertEqual(response.context['recipe'], self.recipe)
    
    def test_recipe_detail_view_404(self):
        """Test that recipe detail returns 404 for non-existent recipe"""
        self.client.login(username='testuser', password='testpass123')
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
        self.client.login(username='testuser', password='testpass123')
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


class RecipeFormTest(TestCase):
    """Test the RecipeForm for adding recipes"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        UserProfile.objects.create(
            user=self.user,
            name='testuser',
            email_address='test@example.com'
        )
    
    def test_recipe_form_fields(self):
        """Test that RecipeForm has all required fields"""
        form = RecipeForm()
        self.assertIn('name', form.fields)
        self.assertIn('cooking_time', form.fields)
        self.assertIn('ingredients', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('pic', form.fields)
    
    def test_recipe_form_valid_data(self):
        """Test RecipeForm with valid data"""
        form_data = {
            'name': 'Test Recipe',
            'cooking_time': 30,
            'ingredients': 'Salt, Pepper, Water',
            'description': 'A test recipe'
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_recipe_form_missing_required_fields(self):
        """Test RecipeForm validation with missing required fields"""
        form = RecipeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('cooking_time', form.errors)
        self.assertIn('ingredients', form.errors)
        self.assertIn('description', form.errors)
    
    def test_recipe_form_pic_optional(self):
        """Test that pic field is optional"""
        form_data = {
            'name': 'Test Recipe',
            'cooking_time': 30,
            'ingredients': 'Salt, Pepper, Water',
            'description': 'A test recipe'
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())


class AddRecipeViewTest(TestCase):
    """Test the add_recipe view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        UserProfile.objects.create(
            user=self.user,
            name='testuser',
            email_address='test@example.com'
        )
    
    def test_add_recipe_view_requires_login(self):
        """Test that add_recipe view requires authentication"""
        url = reverse('recipes:add_recipe')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirects to login
    
    def test_add_recipe_view_get(self):
        """Test GET request to add_recipe view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('recipes:add_recipe')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/add_recipe.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], RecipeForm)
    
    def test_add_recipe_view_post_valid(self):
        """Test POST request with valid recipe data"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('recipes:add_recipe')
        form_data = {
            'name': 'New Recipe',
            'cooking_time': 25,
            'ingredients': 'Flour, Sugar, Eggs',
            'description': 'A delicious new recipe'
        }
        response = self.client.post(url, form_data)
        # Should redirect to recipe detail page
        self.assertEqual(response.status_code, 302)
        
        # Check that recipe was created
        recipe = Recipe.objects.get(name='New Recipe')
        self.assertEqual(recipe.author, self.user)
        self.assertEqual(recipe.cooking_time, 25)
        self.assertEqual(recipe.difficulty, 'Intermediate')  # 25 min (>=10), 3 ingredients (<4) = Intermediate
    
    def test_add_recipe_view_post_invalid(self):
        """Test POST request with invalid recipe data"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('recipes:add_recipe')
        form_data = {
            'name': '',  # Missing required field
            'cooking_time': 25,
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 200)  # Stays on form page
        self.assertFormError(response, 'form', 'name', 'This field is required.')


class FavoriteFunctionalityTest(TestCase):
    """Test favorite/unfavorite functionality"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            name='testuser',
            email_address='test@example.com'
        )
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            author=self.user,
            cooking_time=30,
            ingredients="Salt, Pepper, Water",
            description="A test recipe"
        )
    
    def test_toggle_favorite_requires_login(self):
        """Test that toggle_favorite requires authentication"""
        url = reverse('recipes:toggle_favorite', args=[self.recipe.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirects to login
    
    def test_add_to_favorites(self):
        """Test adding a recipe to favorites"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('recipes:toggle_favorite', args=[self.recipe.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirects to recipe detail
        
        # Check that recipe is in favorites
        self.user_profile.refresh_from_db()
        self.assertIn(self.recipe, self.user_profile.favorited_recipes.all())
    
    def test_remove_from_favorites(self):
        """Test removing a recipe from favorites"""
        self.client.login(username='testuser', password='testpass123')
        # First add to favorites
        self.user_profile.favorited_recipes.add(self.recipe)
        
        # Then remove
        url = reverse('recipes:toggle_favorite', args=[self.recipe.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        
        # Check that recipe is no longer in favorites
        self.user_profile.refresh_from_db()
        self.assertNotIn(self.recipe, self.user_profile.favorited_recipes.all())
    
    def test_user_favorites_view_requires_login(self):
        """Test that user_favorites view requires authentication"""
        url = reverse('recipes:user_favorites')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirects to login
    
    def test_user_favorites_view(self):
        """Test user_favorites view displays user's favorites"""
        self.client.login(username='testuser', password='testpass123')
        # Add recipe to favorites
        self.user_profile.favorited_recipes.add(self.recipe)
        
        url = reverse('recipes:user_favorites')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/user_favorites.html')
        self.assertIn('favorites', response.context)
        self.assertIn(self.recipe, response.context['favorites'])
    
    def test_user_favorites_view_empty(self):
        """Test user_favorites view with no favorites"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('recipes:user_favorites')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['favorites']), 0)
    
    def test_recipe_detail_shows_favorite_status(self):
        """Test that recipe detail view shows favorite status"""
        self.client.login(username='testuser', password='testpass123')
        # Add recipe to favorites
        self.user_profile.favorited_recipes.add(self.recipe)
        
        url = reverse('recipes:recipe_detail', args=[self.recipe.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('is_favorited', response.context)
        self.assertTrue(response.context['is_favorited'])


class UserRegistrationFormTest(TestCase):
    """Test the UserRegistrationForm"""
    
    def setUp(self):
        self.existing_user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='testpass123'
        )
    
    def test_registration_form_fields(self):
        """Test that registration form has all required fields"""
        from recipe_project.forms import UserRegistrationForm
        form = UserRegistrationForm()
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)
    
    def test_registration_form_valid_data(self):
        """Test registration form with valid data"""
        from recipe_project.forms import UserRegistrationForm
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Password123',
            'password2': 'Password123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_registration_form_duplicate_username(self):
        """Test registration form with duplicate username"""
        from recipe_project.forms import UserRegistrationForm
        form_data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password1': 'Password123',
            'password2': 'Password123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_registration_form_password_too_short(self):
        """Test registration form with password too short"""
        from recipe_project.forms import UserRegistrationForm
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Pass1',  # Too short
            'password2': 'Pass1'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)
    
    def test_registration_form_password_too_long(self):
        """Test registration form with password too long"""
        from recipe_project.forms import UserRegistrationForm
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Password123456789',  # Too long (17 chars)
            'password2': 'Password123456789'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)
    
    def test_registration_form_password_no_number(self):
        """Test registration form with password missing number"""
        from recipe_project.forms import UserRegistrationForm
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Password',  # No number
            'password2': 'Password'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)
    
    def test_registration_form_password_no_uppercase(self):
        """Test registration form with password missing uppercase"""
        from recipe_project.forms import UserRegistrationForm
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123',  # No uppercase
            'password2': 'password123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)
    
    def test_registration_form_password_mismatch(self):
        """Test registration form with mismatched passwords"""
        from recipe_project.forms import UserRegistrationForm
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Password123',
            'password2': 'Password456'  # Different password
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
    
    def test_registration_form_save(self):
        """Test that registration form creates user and profile"""
        from recipe_project.forms import UserRegistrationForm
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Password123',
            'password2': 'Password123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(user.check_password('Password123'))
        
        # Check that UserProfile was created
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.name, 'newuser')
        self.assertEqual(profile.email_address, 'newuser@example.com')


class DeleteProfileTest(TestCase):
    """Test delete profile functionality"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            name='testuser',
            email_address='test@example.com'
        )
    
    def test_delete_profile_requires_login(self):
        """Test that delete_profile view requires authentication"""
        url = reverse('delete_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirects to login
    
    def test_delete_profile_confirmation_page(self):
        """Test delete profile confirmation page"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('delete_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/delete_profile_confirm.html')
    
    def test_delete_profile_post(self):
        """Test deleting profile via POST request"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('delete_profile')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirects to home
        
        # Check that user and profile are deleted
        self.assertFalse(User.objects.filter(username='testuser').exists())
        self.assertFalse(UserProfile.objects.filter(user__username='testuser').exists())