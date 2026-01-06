from django.test import TestCase
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
        # Create a test recipe
        Recipe.objects.create(
            name="Test Recipe",
            recipe_id=1,
            author=self.user,
            cooking_time=30,
            ingredients="Salt, Pepper, Water",
            description="A test recipe",
            difficulty="Easy"
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