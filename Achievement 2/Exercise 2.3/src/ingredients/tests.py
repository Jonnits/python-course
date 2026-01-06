from django.test import TestCase
from .models import Ingredient

class IngredientModelTest(TestCase):
    def setUp(self):
        Ingredient.objects.create(
            name="Salt",
            quantity="1 teaspoon"
        )
    
    def test_ingredient_name(self):
        ingredient = Ingredient.objects.get(name="Salt")
        self.assertEqual(ingredient.name, "Salt")
    
    def test_ingredient_str(self):
        ingredient = Ingredient.objects.get(name="Salt")
        self.assertEqual(str(ingredient), "1 teaspoon Salt")