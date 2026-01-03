# Exercise 1.7: Complete Recipe Application with SQLAlchemy
# This application provides a menu-driven interface for managing recipes in a MySQL database

import os
from sqlalchemy import create_engine, Column, Integer, String, func, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import or_
from dotenv import load_dotenv
load_dotenv()

# Part 1: Set Up SQLAlchemy Connection
# Load credentials from environment variables for security
# You can set these in your terminal 

# Get credentials from environment variables (with fallback defaults for development)
MYSQL_USER = os.getenv('MYSQL_USER', 'cf-python')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'eighty1')
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'task_database')

# Create engine object to connect to the database
engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}",
    echo=False  
)

# Create Session class and bind it to the engine
Session = sessionmaker(bind=engine)

# Initialize session object
session = Session()

# Part 2: Create Model and Table
# Store declarative base class
Base = declarative_base()


class Recipe(Base):
    """
    Recipe model class that represents the final_recipes table in the database.
    """
    # Set table name
    __tablename__ = 'final_recipes'
    
    # Define columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))
    
    def __repr__(self):
        """
        Quick representation of the recipe object.
        Returns: String with id, name, and difficulty.
        """
        return f"<Recipe(id={self.id}, name='{self.name}', difficulty='{self.difficulty}')>"
    
    def __str__(self):
        """
        Well-formatted string representation of the recipe.
        Returns: Formatted string with all recipe details.
        """
        output = "\n" + "="*60 + "\n"
        output += f"Recipe: {self.name}\n"
        output += "-"*60 + "\n"
        output += f"Cooking Time: {self.cooking_time} minutes\n"
        output += f"Difficulty: {self.difficulty}\n"
        output += f"Ingredients:\n"
        
        # Split ingredients string into list for better display
        ingredients_list = self.return_ingredients_as_list()
        for ingredient in ingredients_list:
            output += f"\t- {ingredient}\n"
        
        output += "="*60
        return output
    
    def calculate_difficulty(self):
        """
        Calculates the difficulty of the recipe based on cooking time and number of ingredients.
        Updates the self.difficulty attribute.
        """
        num_ingredients = len(self.return_ingredients_as_list())
        
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_ingredients >= 4:
            self.difficulty = "Hard"
    
    def return_ingredients_as_list(self):
        """
        Retrieves the ingredients string as a list.
        Returns: List of ingredients, or empty list if ingredients string is empty.
        """
        if self.ingredients == "":
            return []
        else:
            # Split by comma and space, then strip whitespace from each ingredient
            return [ingredient.strip() for ingredient in self.ingredients.split(", ")]


# Create the table in the database
Base.metadata.create_all(engine)


# Part 3: Define Main Operations as Functions

def create_recipe():
    """
    Function 1: Creates a new recipe and adds it to the database.
    Collects recipe details from user with input validation.
    """
    try:
        # Collect recipe name
        print("\n" + "="*60)
        print("CREATE A NEW RECIPE")
        print("="*60)
        
        name = input("\nEnter the recipe name: ").strip()
        
        # Validate name: check length and ensure it's not empty
        if len(name) == 0:
            print("Error: Recipe name cannot be empty.")
            return
        if len(name) > 50:
            print("Error: Recipe name cannot exceed 50 characters.")
            return
        
        # Collect cooking time
        cooking_time_input = input("Enter the cooking time (in minutes): ").strip()
        
        # Validate cooking time: must be numeric and positive
        if not cooking_time_input.isnumeric():
            print("Error: Cooking time must be a number.")
            return
        
        cooking_time = int(cooking_time_input)
        if cooking_time <= 0:
            print("Error: Cooking time must be a positive number.")
            return
        
        # Collect ingredients
        ingredients = []
        num_ingredients_input = input("How many ingredients does this recipe have? ").strip()
        
        # Validate number of ingredients
        if not num_ingredients_input.isnumeric():
            print("Error: Number of ingredients must be a number.")
            return
        
        num_ingredients = int(num_ingredients_input)
        if num_ingredients <= 0:
            print("Error: Number of ingredients must be at least 1.")
            return
        
        # Collect each ingredient
        for i in range(num_ingredients):
            ingredient = input(f"Enter ingredient {i+1}: ").strip()
            if len(ingredient) > 0:  # Only add non-empty ingredients
                ingredients.append(ingredient)
        
        # Check if we have any ingredients
        if len(ingredients) == 0:
            print("Error: Recipe must have at least one ingredient.")
            return
        
        # Convert ingredients list to comma-separated string
        ingredients_str = ", ".join(ingredients)
        
        # Check total length of ingredients string
        if len(ingredients_str) > 255:
            print("Error: Total length of ingredients cannot exceed 255 characters.")
            return
        
        # Create new Recipe object
        recipe_entry = Recipe(
            name=name,
            ingredients=ingredients_str,
            cooking_time=cooking_time
        )
        
        # Calculate difficulty
        recipe_entry.calculate_difficulty()
        
        # Add to database and commit
        session.add(recipe_entry)
        session.commit()
        
        print(f"\n✓ Recipe '{name}' has been added to the database successfully!")
        
    except Exception as e:
        print(f"\nError creating recipe: {e}")
        session.rollback()


def view_all_recipes():
    """
    Function 2: Displays all recipes in the database.
    """
    try:
        # Retrieve all recipes from database
        recipes = session.query(Recipe).all()
        
        # Check if database is empty
        if len(recipes) == 0:
            print("\n" + "="*60)
            print("No recipes found in the database.")
            print("="*60)
            return
        
        # Display all recipes
        print("\n" + "="*60)
        print("ALL RECIPES")
        print("="*60)
        
        for recipe in recipes:
            print(recipe)
        
    except Exception as e:
        print(f"\nError viewing recipes: {e}")


def search_by_ingredients():
    """
    Function 3: Searches for recipes containing specific ingredients.
    """
    try:
        # Check if table has any entries
        if session.query(Recipe).count() == 0:
            print("\n" + "="*60)
            print("No recipes found in the database.")
            print("="*60)
            return
        
        # Retrieve all ingredients from database
        results = session.query(Recipe.ingredients).all()
        
        # Extract all unique ingredients
        all_ingredients = []
        for (ingredients_str,) in results:
            # Split ingredients string into list
            ingredients_list = [ing.strip() for ing in ingredients_str.split(", ")]
            for ingredient in ingredients_list:
                if ingredient not in all_ingredients and len(ingredient) > 0:
                    all_ingredients.append(ingredient)
        
        # Check if we found any ingredients
        if len(all_ingredients) == 0:
            print("\nNo ingredients found in the database.")
            return
        
        # Display ingredients to user
        print("\n" + "="*60)
        print("AVAILABLE INGREDIENTS")
        print("="*60)
        for index, ingredient in enumerate(all_ingredients, start=1):
            print(f"{index}. {ingredient}")
        
        # Get user input for ingredients to search
        print("\nEnter the numbers of ingredients to search for (separated by spaces):")
        user_input = input("Your selection: ").strip()
        
        # Validate input
        if not user_input:
            print("Error: No selection made.")
            return
        
        # Parse user input into list of numbers
        try:
            selected_numbers = [int(num.strip()) for num in user_input.split()]
        except ValueError:
            print("Error: Please enter valid numbers separated by spaces.")
            return
        
        # Validate that all numbers are within valid range
        if not all(1 <= num <= len(all_ingredients) for num in selected_numbers):
            print(f"Error: Please enter numbers between 1 and {len(all_ingredients)}.")
            return
        
        # Create list of ingredients to search for
        search_ingredients = [all_ingredients[num - 1] for num in selected_numbers]
        
        # Build search conditions using OR logic (recipe contains any of the selected ingredients)
        # Use case-insensitive search by converting both sides to lowercase
        conditions = []
        for ingredient in search_ingredients:
            like_term = f"%{ingredient.lower()}%"
            # Use func.lower() to make the search case-insensitive
            conditions.append(func.lower(Recipe.ingredients).like(like_term))
        
        # Query database with OR conditions
        matching_recipes = session.query(Recipe).filter(or_(*conditions)).all()
        
        # Display results
        if matching_recipes:
            print("\n" + "="*60)
            print(f"RECIPES CONTAINING: {', '.join(search_ingredients)}")
            print("="*60)
            for recipe in matching_recipes:
                print(recipe)
        else:
            print(f"\nNo recipes found containing: {', '.join(search_ingredients)}")
        
    except Exception as e:
        print(f"\nError searching recipes: {e}")


def edit_recipe():
    """
    Function 4: Edits an existing recipe in the database.
    """
    try:
        # Check if any recipes exist
        if session.query(Recipe).count() == 0:
            print("\n" + "="*60)
            print("No recipes found in the database.")
            print("="*60)
            return
        
        # Retrieve id and name for all recipes
        results = session.query(Recipe.id, Recipe.name).all()
        
        # Display available recipes
        print("\n" + "="*60)
        print("AVAILABLE RECIPES")
        print("="*60)
        for recipe_id, name in results:
            print(f"ID: {recipe_id} - {name}")
        
        # Get recipe ID from user
        recipe_id_input = input("\nEnter the ID of the recipe to edit: ").strip()
        
        # Validate input
        if not recipe_id_input.isnumeric():
            print("Error: Recipe ID must be a number.")
            return
        
        recipe_id = int(recipe_id_input)
        
        # Retrieve the recipe
        recipe_to_edit = session.query(Recipe).filter(Recipe.id == recipe_id).first()
        
        if recipe_to_edit is None:
            print(f"Error: Recipe with ID {recipe_id} not found.")
            return
        
        # Display recipe details
        print("\n" + "="*60)
        print("RECIPE TO EDIT")
        print("="*60)
        print(f"1. Name: {recipe_to_edit.name}")
        print(f"2. Ingredients: {recipe_to_edit.ingredients}")
        print(f"3. Cooking Time: {recipe_to_edit.cooking_time} minutes")
        
        # Get attribute to edit
        attribute_choice = input("\nEnter the number of the attribute to edit (1-3): ").strip()
        
        # Edit based on user choice
        if attribute_choice == "1":
            # Edit name
            new_name = input("Enter the new name: ").strip()
            if len(new_name) == 0:
                print("Error: Recipe name cannot be empty.")
                return
            if len(new_name) > 50:
                print("Error: Recipe name cannot exceed 50 characters.")
                return
            recipe_to_edit.name = new_name
            
        elif attribute_choice == "2":
            # Edit ingredients
            num_ingredients_input = input("How many ingredients does this recipe have? ").strip()
            if not num_ingredients_input.isnumeric():
                print("Error: Number of ingredients must be a number.")
                return
            
            num_ingredients = int(num_ingredients_input)
            if num_ingredients <= 0:
                print("Error: Number of ingredients must be at least 1.")
                return
            
            ingredients = []
            for i in range(num_ingredients):
                ingredient = input(f"Enter ingredient {i+1}: ").strip()
                if len(ingredient) > 0:
                    ingredients.append(ingredient)
            
            if len(ingredients) == 0:
                print("Error: Recipe must have at least one ingredient.")
                return
            
            ingredients_str = ", ".join(ingredients)
            if len(ingredients_str) > 255:
                print("Error: Total length of ingredients cannot exceed 255 characters.")
                return
            
            recipe_to_edit.ingredients = ingredients_str
            
        elif attribute_choice == "3":
            # Edit cooking time
            new_cooking_time_input = input("Enter the new cooking time (in minutes): ").strip()
            if not new_cooking_time_input.isnumeric():
                print("Error: Cooking time must be a number.")
                return
            
            new_cooking_time = int(new_cooking_time_input)
            if new_cooking_time <= 0:
                print("Error: Cooking time must be a positive number.")
                return
            
            recipe_to_edit.cooking_time = new_cooking_time
            
        else:
            print("Error: Invalid choice. Please enter 1, 2, or 3.")
            return
        
        # Recalculate difficulty after any edit
        recipe_to_edit.calculate_difficulty()
        
        # Commit changes
        session.commit()
        print(f"\n✓ Recipe ID {recipe_id} has been updated successfully!")
        
    except Exception as e:
        print(f"\nError editing recipe: {e}")
        session.rollback()


def delete_recipe():
    """
    Function 5: Deletes a recipe from the database.
    """
    try:
        # Check if any recipes exist
        if session.query(Recipe).count() == 0:
            print("\n" + "="*60)
            print("No recipes found in the database.")
            print("="*60)
            return
        
        # Retrieve id and name for all recipes
        results = session.query(Recipe.id, Recipe.name).all()
        
        # Display available recipes
        print("\n" + "="*60)
        print("AVAILABLE RECIPES")
        print("="*60)
        for recipe_id, name in results:
            print(f"ID: {recipe_id} - {name}")
        
        # Get recipe ID from user
        recipe_id_input = input("\nEnter the ID of the recipe to delete: ").strip()
        
        # Validate input
        if not recipe_id_input.isnumeric():
            print("Error: Recipe ID must be a number.")
            return
        
        recipe_id = int(recipe_id_input)
        
        # Retrieve the recipe
        recipe_to_delete = session.query(Recipe).filter(Recipe.id == recipe_id).first()
        
        if recipe_to_delete is None:
            print(f"Error: Recipe with ID {recipe_id} not found.")
            return
        
        # Display recipe to be deleted
        print("\n" + "="*60)
        print("RECIPE TO DELETE")
        print("="*60)
        print(recipe_to_delete)
        
        # Confirm deletion
        confirm = input("\nAre you sure you want to delete this recipe? (yes/no): ").strip().lower()
        
        if confirm == "yes":
            session.delete(recipe_to_delete)
            session.commit()
            print(f"\n✓ Recipe ID {recipe_id} has been deleted successfully!")
        else:
            print("Deletion cancelled.")
        
    except Exception as e:
        print(f"\nError deleting recipe: {e}")
        session.rollback()


# Part 4: Design Main Menu
def main_menu():
    """
    Main menu function that displays options and handles user input.
    Runs in a while loop until user chooses to quit.
    """
    while True:
        print("\n" + "="*60)
        print("RECIPE APPLICATION - MAIN MENU")
        print("="*60)
        print("Pick a choice:")
        print("\t1. Create a new recipe")
        print("\t2. View all recipes")
        print("\t3. Search for recipes by ingredients")
        print("\t4. Edit a recipe")
        print("\t5. Delete a recipe")
        print("\tType 'quit' to exit the application")
        print("="*60)
        
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "quit":
            print("\n" + "="*60)
            print("Thank you for using the Recipe Application!")
            print("="*60)
            # Close session and engine
            session.close()
            engine.dispose()
            break
        else:
            print("\n⚠ Invalid choice. Please enter a number between 1-5 or 'quit'.")


# Part 5: Run the Application
if __name__ == '__main__':
    try:
        # Test database connection
        session.execute(text("SELECT 1"))
        print("✓ Successfully connected to the database!")
        
        # Start main menu
        main_menu()
        
    except Exception as e:
        print(f"\n✗ Error connecting to database: {e}")
        print("Please check your MySQL server is running and credentials are correct.")
        session.close()
        engine.dispose()

