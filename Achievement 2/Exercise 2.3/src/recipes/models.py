from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=120)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cooking_time = models.IntegerField(help_text="Time in minutes")
    ingredients = models.TextField()
    description = models.TextField()
    difficulty = models.CharField(max_length=20, blank=True)
    pic = models.ImageField(upload_to='recipe_pics/', blank=True, null=True)
    
    def calculate_difficulty(self):
        """Calculate recipe difficulty based on cooking time and number of ingredients"""
        ingredients_list = self.get_ingredients_list()
        num_ingredients = len(ingredients_list)
        
        if self.cooking_time < 10 and num_ingredients < 4:
            return "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            return "Intermediate"
        else:  # cooking_time >= 10 and num_ingredients >= 4
            return "Hard"
    
    def get_ingredients_list(self):
        """Return ingredients as a sorted list"""
        if self.ingredients:
            ingredients = [ingredient.strip() for ingredient in self.ingredients.split(',')]
            return sorted(ingredients)
        return []
    
    def save(self, *args, **kwargs):
        """Override save to calculate difficulty before saving"""
        self.difficulty = self.calculate_difficulty()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name