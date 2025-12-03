# This script loads recipes from a binary file and allows searching by ingredient

import pickle

def display_recipe(recipe):
    """
    Displays a recipe with all its attributes.
    Takes a recipe dictionary as argument.
    """
    print("\n" + "="*50)
    print(f"Recipe: {recipe['name']}")
    print(f"  Cooking Time: {recipe['cooking_time']} minutes")
    print(f"  Difficulty: {recipe['difficulty']}")
    print(f"  Ingredients:")
    for ingredient in recipe['ingredients']:
        print(f"    - {ingredient}")

def search_ingredient(data):
    """
    Searches for recipes containing a specific ingredient.
    Takes a dictionary containing recipes_list and all_ingredients as argument.
    """
    # Display all available ingredients with numbers
    print("\nAvailable ingredients:")
    all_ingredients = data.get('all_ingredients', [])
    
    if not all_ingredients:
        print("No ingredients available.")
        return
    
    # Use enumerate to display ingredients with numbers
    for index, ingredient in enumerate(all_ingredients, start=1):
        print(f"  {index}. {ingredient}")
    
    # Try block to get user input and search
    try:
        choice = int(input("\nEnter the number of the ingredient you'd like to search for: "))
        
        if choice < 1 or choice > len(all_ingredients):
            raise ValueError("Invalid choice number")
        
        # Get the ingredient at the chosen index (convert to 0-based index)
        ingredient_searched = all_ingredients[choice - 1]
        
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return
    else:
        # Search through recipes and display those containing the ingredient
        recipes_list = data.get('recipes_list', [])
        found_recipes = False
        
        print(f"\nRecipes containing '{ingredient_searched}':")
        print("="*50)
        
        for recipe in recipes_list:
            if ingredient_searched in recipe['ingredients']:
                display_recipe(recipe)
                found_recipes = True
        
        if not found_recipes:
            print(f"No recipes found containing '{ingredient_searched}'.")

# Main code
if __name__ == '__main__':
    # Ask user for filename
    filename = input("Enter the filename where your recipes are stored: ")
    
    # Try block to open and load the file
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
    except FileNotFoundError:
        print(f"File '{filename}' not found. Please make sure the file exists.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    else:
        # File loaded successfully, call search_ingredient function
        search_ingredient(data)

