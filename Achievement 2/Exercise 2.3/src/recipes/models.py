from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=120)
    recipe_id = models.IntegerField(primary_key=True, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cooking_time = models.IntegerField(help_text="Time in minutes")
    ingredients = models.TextField()
    description = models.TextField()
    difficulty = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name