from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50, help_text="e.g., '2 cups', '500g', '1 tablespoon'")
    
    def __str__(self):
        return f"{self.quantity} {self.name}"
