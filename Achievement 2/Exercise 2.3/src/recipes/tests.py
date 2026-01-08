from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe


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