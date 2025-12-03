recipes_list = []
ingredients_list = []

def take_recipe():
    """
    Takes input from the user for recipe details and returns a dictionary.
    """
    name = str(input("Enter the name of the recipe: "))
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    
    # Get ingredients from user
    ingredients = []
    num_ingredients = int(input("How many ingredients does this recipe have? "))
    for i in range(num_ingredients):
        ingredient = str(input(f"Enter ingredient {i+1}: "))
        ingredients.append(ingredient)
    
    # Create recipe dictionary
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients
    }
    
    return recipe


if __name__ == '__main__':
    # Ask user how many recipes they would like to enter
    n = int(input("How many recipes would you like to enter? "))
    
    # Run a for loop n times to collect recipes
    for i in range(n):
        print(f"\n--- Recipe {i+1} ---")
        recipe = take_recipe()
        
        # Loop through recipe's ingredients and add to ingredients_list if not present
        for ingredient in recipe['ingredients']:
            if ingredient not in ingredients_list:
                ingredients_list.append(ingredient)
        
        # Append recipe to recipes_list
        recipes_list.append(recipe)
    
    # Display all recipes with difficulty calculation
    print("\n" + "="*50)
    print("RECIPES LIST")
    print("="*50)
    
    for recipe in recipes_list:
        # Determine difficulty based on cooking_time and number of ingredients
        cooking_time = recipe['cooking_time']
        num_ingredients = len(recipe['ingredients'])
        
        if cooking_time < 10 and num_ingredients < 4:
            difficulty = "Easy"
        elif cooking_time < 10 and num_ingredients >= 4:
            difficulty = "Medium"
        elif cooking_time >= 10 and num_ingredients < 4:
            difficulty = "Intermediate"
        elif cooking_time >= 10 and num_ingredients >= 4:
            difficulty = "Hard"
        
        # Display recipe details
        print(f"\nRecipe: {recipe['name']}")
        print(f"  Cooking Time: {recipe['cooking_time']} minutes")
        print(f"  Ingredients: {', '.join(recipe['ingredients'])}")
        print(f"  Difficulty: {difficulty}")
    
    # Display all ingredients in alphabetical order
    print("\n" + "="*50)
    print("INGREDIENTS LIST")
    print("="*50)
    print("\nAll ingredients (alphabetically sorted):")
    for ingredient in sorted(ingredients_list):
        print(f"  - {ingredient}")

