from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email_address = models.EmailField()
    favorited_recipes = models.ManyToManyField('recipes.Recipe', related_name='favorited_by', blank=True)
    submitted_recipes = models.ManyToManyField('recipes.Recipe', related_name='submitted_by', blank=True)
    
    def __str__(self):
        return self.name
