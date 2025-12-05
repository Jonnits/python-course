# Exercise 1.6: Recipe Management with MySQL Database

import mysql.connector
from mysql.connector import Error

# Part 1: Create & Connect Database
def connect_to_database():
    """Connects to MySQL server and sets up the database and table."""
    try:
        # Initialize connection
        conn = mysql.connector.connect(
            host='localhost',
            user='cf-python',
            passwd='eighty1'
        )
        
        # Initialize cursor
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
        
        # Use the database
        cursor.execute("USE task_database")
        
        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Recipes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50),
                ingredients VARCHAR(255),
                cooking_time INT,
                difficulty VARCHAR(20)
            )
        """)
        
        return conn, cursor
    
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None, None


# Part 3: Calculate Difficulty Function
def calculate_difficulty(cooking_time, ingredients):
    """
    Calculates the difficulty of a recipe based on cooking time and number of ingredients.
    
    Args:
        cooking_time (int): Cooking time in minutes
        ingredients (list): List of ingredients
        
    Returns:
        str: Difficulty level (Easy, Medium, Intermediate, or Hard)
    """
    num_ingredients = len(ingredients)
    
    if cooking_time < 10 and num_ingredients < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and num_ingredients >= 4:
        difficulty = "Hard"
    
    return difficulty


# Part 3: Create Recipe Function
def create_recipe(conn, cursor):
    """Creates a new recipe and adds it to the database."""
    try:
        # Collect recipe details
        name = input("\nEnter the recipe name: ")
        cooking_time = int(input("Enter the cooking time (in minutes): "))
        
        # Collect ingredients
        ingredients = []
        num_ingredients = int(input("How many ingredients does this recipe have? "))
        for i in range(num_ingredients):
            ingredient = input(f"Enter ingredient {i+1}: ")
            ingredients.append(ingredient)
        
        # Calculate difficulty
        difficulty = calculate_difficulty(cooking_time, ingredients)
        
        # Convert ingredients list to comma-separated string
        ingredients_str = ", ".join(ingredients)
        
        # Build and execute INSERT query
        query = """
            INSERT INTO Recipes (name, ingredients, cooking_time, difficulty)
            VALUES (%s, %s, %s, %s)
        """
        values = (name, ingredients_str, cooking_time, difficulty)
        
        cursor.execute(query, values)
        conn.commit()
        
        print(f"\nRecipe '{name}' has been added to the database successfully!")
    
    except Error as e:
        print(f"Error creating recipe: {e}")
    except ValueError:
        print("Invalid input. Please enter a valid number for cooking time and ingredient count.")


# Part 4: Search Recipe Function
def search_recipe(conn, cursor):
    """Searches for recipes containing a specific ingredient."""
    try:
        # Get all ingredients from the database
        cursor.execute("SELECT ingredients FROM Recipes")
        results = cursor.fetchall()
        
        # Extract all unique ingredients
        all_ingredients = []
        for row in results:
            ingredients_str = row[0]  # Get the ingredients string from the tuple
            ingredients_list = [ing.strip() for ing in ingredients_str.split(",")]
            for ingredient in ingredients_list:
                if ingredient not in all_ingredients:
                    all_ingredients.append(ingredient)
        
        # Display ingredients to user
        if not all_ingredients:
            print("\nNo ingredients found in the database.")
            return
        
        print("\nAvailable ingredients:")
        for index, ingredient in enumerate(all_ingredients, start=1):
            print(f"  {index}. {ingredient}")
        
        # Get user's choice
        try:
            choice = int(input("\nEnter the number of the ingredient to search for: "))
            if choice < 1 or choice > len(all_ingredients):
                print("Invalid choice.")
                return
            
            search_ingredient = all_ingredients[choice - 1]
            
            # Search for recipes containing the ingredient
            query = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
            search_pattern = f"%{search_ingredient}%"
            cursor.execute(query, (search_pattern,))
            results = cursor.fetchall()
            
            # Display results
            if results:
                print(f"\nRecipes containing '{search_ingredient}':")
                print("="*60)
                for row in results:
                    print(f"\nID: {row[0]}")
                    print(f"Name: {row[1]}")
                    print(f"Ingredients: {row[2]}")
                    print(f"Cooking Time: {row[3]} minutes")
                    print(f"Difficulty: {row[4]}")
                    print("-"*60)
            else:
                print(f"\nNo recipes found containing '{search_ingredient}'.")
        
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    except Error as e:
        print(f"Error searching recipes: {e}")


# Part 5: Update Recipe Function
def update_recipe(conn, cursor):
    """Updates an existing recipe in the database."""
    try:
        # Display all recipes
        cursor.execute("SELECT * FROM Recipes")
        results = cursor.fetchall()
        
        if not results:
            print("\nNo recipes found in the database.")
            return
        
        print("\nAll recipes in the database:")
        print("="*60)
        for row in results:
            print(f"\nID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Ingredients: {row[2]}")
            print(f"Cooking Time: {row[3]} minutes")
            print(f"Difficulty: {row[4]}")
            print("-"*60)
        
        # Get recipe ID to update
        recipe_id = int(input("\nEnter the ID of the recipe to update: "))
        
        # Get column to update
        print("\nColumns available for update:")
        print("  1. name")
        print("  2. cooking_time")
        print("  3. ingredients")
        
        column_choice = input("Enter the number of the column to update: ")
        
        if column_choice == "1":
            column_name = "name"
            new_value = input("Enter the new name: ")
            query = f"UPDATE Recipes SET {column_name} = %s WHERE id = %s"
            cursor.execute(query, (new_value, recipe_id))
        
        elif column_choice == "2":
            column_name = "cooking_time"
            new_value = int(input("Enter the new cooking time (in minutes): "))
            query = f"UPDATE Recipes SET {column_name} = %s WHERE id = %s"
            cursor.execute(query, (new_value, recipe_id))
            
            # Recalculate difficulty
            cursor.execute("SELECT ingredients FROM Recipes WHERE id = %s", (recipe_id,))
            result = cursor.fetchone()
            if result:
                ingredients_str = result[0]
                ingredients_list = [ing.strip() for ing in ingredients_str.split(",")]
                difficulty = calculate_difficulty(new_value, ingredients_list)
                cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (difficulty, recipe_id))
        
        elif column_choice == "3":
            column_name = "ingredients"
            num_ingredients = int(input("How many ingredients does this recipe have? "))
            ingredients = []
            for i in range(num_ingredients):
                ingredient = input(f"Enter ingredient {i+1}: ")
                ingredients.append(ingredient)
            new_value = ", ".join(ingredients)
            query = f"UPDATE Recipes SET {column_name} = %s WHERE id = %s"
            cursor.execute(query, (new_value, recipe_id))
            
            # Recalculate difficulty
            cursor.execute("SELECT cooking_time FROM Recipes WHERE id = %s", (recipe_id,))
            result = cursor.fetchone()
            if result:
                cooking_time = result[0]
                difficulty = calculate_difficulty(cooking_time, ingredients)
                cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (difficulty, recipe_id))
        
        else:
            print("Invalid choice.")
            return
        
        conn.commit()
        print(f"\nRecipe ID {recipe_id} has been updated successfully!")
    
    except Error as e:
        print(f"Error updating recipe: {e}")
    except ValueError:
        print("Invalid input. Please enter valid numbers.")


# Part 6: Delete Recipe Function
def delete_recipe(conn, cursor):
    """Deletes a recipe from the database."""
    try:
        # Display all recipes
        cursor.execute("SELECT * FROM Recipes")
        results = cursor.fetchall()
        
        if not results:
            print("\nNo recipes found in the database.")
            return
        
        print("\nAll recipes in the database:")
        print("="*60)
        for row in results:
            print(f"\nID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Ingredients: {row[2]}")
            print(f"Cooking Time: {row[3]} minutes")
            print(f"Difficulty: {row[4]}")
            print("-"*60)
        
        # Get recipe ID to delete
        recipe_id = int(input("\nEnter the ID of the recipe to delete: "))
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete recipe ID {recipe_id}? (yes/no): ")
        if confirm.lower() != "yes":
            print("Deletion cancelled.")
            return
        
        # Delete the recipe
        query = "DELETE FROM Recipes WHERE id = %s"
        cursor.execute(query, (recipe_id,))
        conn.commit()
        
        print(f"\nRecipe ID {recipe_id} has been deleted successfully!")
    
    except Error as e:
        print(f"Error deleting recipe: {e}")
    except ValueError:
        print("Invalid input. Please enter a valid recipe ID.")


# Part 2: Main Menu Function
def main_menu(conn, cursor):
    """Displays the main menu and handles user choices."""
    while True:
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("Pick a choice:")
        print("  1. Create a new recipe")
        print("  2. Search for a recipe by ingredient")
        print("  3. Update an existing recipe")
        print("  4. Delete a recipe")
        print("  Type 'quit' to exit the program")
        print("="*60)
        
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        elif choice == "quit":
            print("\nExiting the program. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")


# Main code
if __name__ == '__main__':
    # Connect to database
    conn, cursor = connect_to_database()
    
    if conn and cursor:
        print("Successfully connected to MySQL database!")
        
        # Run main menu
        main_menu(conn, cursor)
        
        # Close connection
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("\nMySQL connection is closed.")
    else:
        print("Failed to connect to MySQL database. Please check your connection settings.")

