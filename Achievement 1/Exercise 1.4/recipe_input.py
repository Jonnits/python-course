# This script takes recipes from the user and stores them in a binary file using pickle

import pickle

def calc_difficulty(cooking_time, num_ingredients):
    if cooking_time < 10 and num_ingredients < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and num_ingredients >= 4:
        difficulty = "Hard"
    
    return difficulty

def take_recipe():
    name = str(input("Enter the name of the recipe: "))
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    
    # Get ingredients from user
    ingredients = []
    num_ingredients = int(input("How many ingredients does this recipe have? "))
    for i in range(num_ingredients):
        ingredient = str(input(f"Enter ingredient {i+1}: "))
        ingredients.append(ingredient)
    
    # Calculate difficulty
    difficulty = calc_difficulty(cooking_time, len(ingredients))
    
    # Create recipe dictionary
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
        'difficulty': difficulty
    }
    
    return recipe

# Main code
if __name__ == '__main__':
    # Ask user for filename
    filename = input("Enter the filename where you'd like to store your recipes: ")
    
    # Try-except-else-finally block to handle file operations
    try:
        file = open(filename, 'rb')
        data = pickle.load(file)
    except FileNotFoundError:
        # File doesn't exist, create new data structure
        print(f"File '{filename}' not found. Creating a new file.")
        data = {
            'recipes_list': [],
            'all_ingredients': []
        }
    except Exception as e:
        # Handle any other exceptions
        print(f"An error occurred: {e}")
        print("Creating a new file.")
        data = {
            'recipes_list': [],
            'all_ingredients': []
        }
    else:
        # File was successfully opened, close it
        file.close()
    finally:
        # Extract values from dictionary into separate lists
        recipes_list = data.get('recipes_list', [])
        all_ingredients = data.get('all_ingredients', [])
    
    # Ask user how many recipes they'd like to enter
    n = int(input("\nHow many recipes would you like to enter? "))
    
    # Loop to collect recipes
    for i in range(n):
        print(f"\n--- Recipe {i+1} ---")
        recipe = take_recipe()
        
        # Add recipe to recipes_list
        recipes_list.append(recipe)
        
        # Loop through recipe's ingredients and add to all_ingredients if not present
        for ingredient in recipe['ingredients']:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)
    
    # Gather updated lists into dictionary
    data = {
        'recipes_list': recipes_list,
        'all_ingredients': all_ingredients
    }
    
    # Open file in write mode and save data using pickle
    with open(filename, 'wb') as file:
        pickle.dump(data, file)
    
    print(f"\nRecipes have been saved to '{filename}' successfully!")

