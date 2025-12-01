# Exercise 1.2: Recipe Data Structures

## Overview
This exercise focuses on building data structures to store recipe information for a Recipe app. The task involves creating individual recipe structures and an outer structure to store multiple recipes sequentially.

## Objectives
- Create a data structure to store individual recipe information
- Create an outer structure to store multiple recipes
- Understand when to use dictionaries vs. lists vs. tuples
- Practice working with nested data structures

## What Was Accomplished

1. **Created recipe_1**: A dictionary structure containing:
   - `name` (str): Recipe name
   - `cooking_time` (int): Cooking time in minutes
   - `ingredients` (list): List of ingredients as strings

2. **Created all_recipes**: A list structure to store multiple recipes sequentially

3. **Added 5 recipes total**: Created recipe_1 through recipe_5 and added them to all_recipes

4. **Printed ingredients**: Displayed the ingredients list for each recipe

## Project Structure

```
Exercise 1.2/
├── README.md              # This file
├── learning_journal.md    # Learning journal documenting the exercise
├── Step 1.png            # Screenshot of creating recipe_1
├── Step 2.png            # Screenshot of creating all_recipes
├── Step 3.png            # Screenshot of adding 4 more recipes
└── Step 4.png            # Screenshot of printing ingredients
```

## Data Structure Choices

### For recipe_1 (individual recipe structure)
I chose to use a **dictionary** for storing individual recipe information because it provides key-value pairs that allow for named, semantic access to recipe attributes. Unlike tuples or lists, dictionaries enable accessing data by meaningful keys (e.g., `recipe_1['name']`) rather than positional indices, which makes the code more readable and maintainable. Dictionaries also offer flexibility for future modifications, such as adding new recipe attributes without restructuring the entire data model.

### For all_recipes (outer structure)
I chose to use a **list** for storing multiple recipes because it provides sequential storage with the ability to append, modify, and iterate through recipes easily. Lists maintain insertion order and allow for dynamic growth as new recipes are added. This sequential nature makes it straightforward to access recipes by index, iterate through all recipes, and perform operations like printing ingredients for each recipe in the collection.

## How to Run

This exercise was completed in an IPython shell. To replicate:

1. Activate your virtual environment:
   ```bash
   source ~/.virtualenvs/cf-python-base/bin/activate
   ```

2. Launch IPython:
   ```bash
   ipython
   ```

3. Follow the steps shown in the screenshots (Step 1.png through Step 4.png)

## Screenshots

- **Step 1**: Creating recipe_1 (Tea recipe)
- **Step 2**: Creating all_recipes and adding recipe_1
- **Step 3**: Creating and adding 4 additional recipes
- **Step 4**: Printing ingredients for all recipes

## Key Learnings

- Understanding when to use dictionaries vs. lists vs. tuples
- Working with nested data structures
- Building a foundation for a Recipe app data model
- Accessing nested data using bracket notation

## Requirements

- Python 3.8.7
- IPython 8.12.3
- Virtual environment (cf-python-base)

