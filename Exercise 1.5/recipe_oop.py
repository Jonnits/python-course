class Recipe:

    # Class variable to track all ingredients across all recipes
    all_ingredients = []
    
    def __init__(self, name):
        """
        Initialize a Recipe object.
        
        Args:
            name (str): The name of the recipe
        """
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = None
    
    # Getter and setter methods for name
    def get_name(self):
        """Returns the name of the recipe."""
        return self.name
    
    def set_name(self, name):
        """Sets the name of the recipe."""
        self.name = name
    
    # Getter and setter methods for cooking_time
    def get_cooking_time(self):
        """Returns the cooking time of the recipe."""
        return self.cooking_time
    
    def set_cooking_time(self, cooking_time):
        """Sets the cooking time of the recipe."""
        self.cooking_time = cooking_time
    
    def add_ingredients(self, *ingredients):
        """
        Adds ingredients to the recipe.
        Takes variable-length arguments and adds them to the ingredients list.
        Calls update_all_ingredients() after adding ingredients.
        
        Args:
            *ingredients: Variable number of ingredient strings
        """
        for ingredient in ingredients:
            if ingredient not in self.ingredients:
                self.ingredients.append(ingredient)
        self.update_all_ingredients()
    
    def get_ingredients(self):
        """Returns the list of ingredients."""
        return self.ingredients
    
    def calculate_difficulty(self):
        """
        Calculates the difficulty of the recipe based on cooking time and number of ingredients.
        Updates the difficulty attribute.
        """
        num_ingredients = len(self.ingredients)
        
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_ingredients >= 4:
            self.difficulty = "Hard"
    
    def get_difficulty(self):
        """
        Returns the difficulty of the recipe.
        Calls calculate_difficulty() if difficulty hasn't been calculated yet.
        """
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty
    
    def search_ingredient(self, ingredient):
        """
        Searches for an ingredient in the recipe.
        
        Args:
            ingredient (str): The ingredient to search for
            
        Returns:
            bool: True if ingredient is found, False otherwise
        """
        return ingredient in self.ingredients
    
    def update_all_ingredients(self):
        """
        Updates the class variable all_ingredients with ingredients from this recipe.
        Only adds ingredients that aren't already present.
        """
        for ingredient in self.ingredients:
            if ingredient not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)
    
    def __str__(self):
        """
        Returns a string representation of the recipe.
        """
        output = "\n" + "="*50 + "\n"
        output += f"Recipe: {self.name}\n"
        output += f"Cooking Time: {self.cooking_time} minutes\n"
        output += f"Difficulty: {self.get_difficulty()}\n"
        output += "Ingredients:\n"
        for ingredient in self.ingredients:
            output += f"  - {ingredient}\n"
        output += "="*50
        return output


def recipe_search(data, search_term):
    """
    Searches for recipes containing a specific ingredient.
    
    Args:
        data (list): List of Recipe objects to search through
        search_term (str): The ingredient to search for
    """
    print(f"\nRecipes containing '{search_term}':")
    print("="*50)
    
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)


# Main code
if __name__ == '__main__':
    # Create Tea recipe
    tea = Recipe("Tea")
    tea.add_ingredients("Tea Leaves", "Sugar", "Water")
    tea.set_cooking_time(5)
    print(tea)
    
    # Create Coffee recipe
    coffee = Recipe("Coffee")
    coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
    coffee.set_cooking_time(5)
    print(coffee)
    
    # Create Cake recipe
    cake = Recipe("Cake")
    cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
    cake.set_cooking_time(50)
    print(cake)
    
    # Create Banana Smoothie recipe
    banana_smoothie = Recipe("Banana Smoothie")
    banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
    banana_smoothie.set_cooking_time(5)
    print(banana_smoothie)
    
    # Create list of recipes
    recipes_list = [tea, coffee, cake, banana_smoothie]
    
    # Search for recipes containing specific ingredients
    print("\n" + "="*50)
    print("SEARCHING FOR RECIPES BY INGREDIENT")
    print("="*50)
    
    recipe_search(recipes_list, "Water")
    recipe_search(recipes_list, "Sugar")
    recipe_search(recipes_list, "Bananas")

