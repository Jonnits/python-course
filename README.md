# CareerFoundry Python Course

This repository contains my work for the CareerFoundry Python course, organized by exercise.

## Exercise 1.1: Python Environment Setup and Basic Scripting

### Overview
This exercise focused on setting up a Python development environment, creating basic Python scripts, and learning about virtual environments and package management.

### What Was Accomplished

1. **Python Installation**: Verified Python 3.8.7 installation
2. **Virtual Environment Setup**: Created a virtual environment named `cf-python-base` using Python 3.8.7
3. **Basic Script Creation**: Created `add.py` - a script that takes two user inputs and adds them together
4. **IPython Installation**: Set up IPython shell in the virtual environment for enhanced interactive Python development
5. **Requirements File**: Generated `requirements.txt` to document all installed packages
6. **Environment Replication**: Created a second environment `cf-python-copy` and installed packages from `requirements.txt` to demonstrate environment portability

### Project Structure

```
.
└── Exercise 1.1/
    ├── add.py              # Script that adds two user-input numbers
    ├── hello.py            # Simple "Hello, World!" script
    └── requirements.txt    # List of installed packages and versions
```

### Setup Instructions

#### 1. Create and Activate Virtual Environment

```bash
# Create virtual environment with Python 3.8.7
python3.8 -m venv ~/.virtualenvs/cf-python-base

# Activate the environment
cd ~/.virtualenvs/cf-python-base/bin
source activate
```

#### 2. Install Dependencies

```bash
# Navigate to project directory
cd /path/to/this/repository/Exercise\ 1.1/

# Install packages from requirements.txt
pip install -r requirements.txt
```

#### 3. Verify Installation

```bash
# Check Python version
python --version

# Verify IPython installation
ipython --version
```

### Running the Scripts

#### Run add.py
```bash
python Exercise\ 1.1/add.py
```
The script will prompt you to enter two numbers, then display their sum.

#### Run hello.py
```bash
python Exercise\ 1.1/hello.py
```
This will print "Hello, World!" to the console.

#### Launch IPython Shell
```bash
ipython
```

### Requirements

- Python 3.8.7
- pip (Python package installer)
- Virtual environment support (venv module)

### Installed Packages

The following packages are installed in the virtual environment (see `Exercise 1.1/requirements.txt` for complete list):

- **ipython** (8.12.3) - Enhanced interactive Python shell
- Dependencies: traitlets, jedi, prompt-toolkit, pygments, and others

### Notes

- All scripts were developed and tested in a virtual environment to maintain project isolation
- The requirements.txt file ensures consistent package versions across different environments
- This exercise demonstrates best practices for Python project setup and dependency management

## Exercise 1.2: Recipe Data Structures

### Overview
This exercise focuses on building data structures to store recipe information for a Recipe app. The task involves creating individual recipe structures and an outer structure to store multiple recipes sequentially.

### What Was Accomplished

1. **Created recipe_1**: A dictionary structure for storing individual recipe information (name, cooking_time, ingredients)
2. **Created all_recipes**: A list structure to store multiple recipes sequentially
3. **Added 5 more recipes**: Created recipe_1 through recipe_6 and added them to all_recipes
4. **Printed ingredients**: Displayed the ingredients list for each recipe as separate lists

### Project Structure

```
.
└── Exercise 1.2/
    ├── learning_journal.md    # Learning journal
    ├── 1. Activated virtual environment.png            # Screenshot: Activating virtual environment
    ├── 2. Activated IPython.png            # Screenshot: Activating IPython
    ├── 3. Recipe 1 structure.png            # Screenshot: Creating structure for Recipe 1
    ├── 4. All recipes inc. Recipe 1.png            # Screenshot: Printing 'all_recipes' to show successful addition of Recipe 1
    ├── 5. 5 more recipes in All recipes.png            # Screenshot: Adding 5 more drink recipes to 'all-recipes' and showing successful addition
    └── 6. All recipe ingredients.png            # Screenshot: Printing ingredients from all recipes
```

### Data Structure Choices

**For recipe_1 (individual recipe structure):**
I chose to use a dictionary for storing individual recipe information because it provides key-value pairs that allow for named, semantic access to recipe attributes. Unlike tuples or lists, dictionaries enable accessing data by meaningful keys (e.g., `recipe_1['name']`) rather than positional indices, which makes the code more readable and maintainable. Dictionaries also offer flexibility for future modifications, such as adding new recipe attributes without restructuring the entire data model.

**For all_recipes (outer structure):**
I chose to use a list for storing multiple recipes because it provides sequential storage with the ability to append, modify, and iterate through recipes easily. Lists maintain insertion order and allow for dynamic growth as new recipes are added. This sequential nature makes it straightforward to access recipes by index, iterate through all recipes, and perform operations like printing ingredients for each recipe in the collection.

## Exercise 1.3: Recipe Management with Difficulty Calculation

### Overview
This exercise builds upon Exercise 1.2 by creating an interactive recipe management system that collects recipes from user input, tracks unique ingredients across all recipes, calculates recipe difficulty based on cooking time and ingredient count, and displays organized recipe information.

### What Was Accomplished

1. **Created `take_recipe()` function**: A reusable function that collects recipe details (name, cooking time, ingredients) from user input and returns a dictionary
2. **Dynamic recipe collection**: Implemented a loop-based system to collect any number of recipes from the user
3. **Unique ingredient tracking**: Built logic to maintain a master list of all unique ingredients across all recipes
4. **Difficulty calculation**: Implemented a multi-condition algorithm to automatically calculate recipe difficulty:
   - Easy: < 10 minutes AND < 4 ingredients
   - Medium: < 10 minutes AND ≥ 4 ingredients
   - Intermediate: ≥ 10 minutes AND < 4 ingredients
   - Hard: ≥ 10 minutes AND ≥ 4 ingredients
5. **Formatted recipe display**: Created organized output showing all recipes with their details and difficulty levels
6. **Alphabetized ingredients list**: Displayed all unique ingredients in alphabetical order

### Project Structure

```
.
└── Exercise 1.3/
    ├── Exercise_1.3.py                              # Main script for recipe management
    ├── learning_journal.md                          # Learning journal
    ├── 1. Activating venv and opening IPython.png   # Screenshot: Activating virtual environment and opening IPython
    ├── 2. Entering new recipe.png                   # Screenshot: Entering a new recipe
    └── 3. Entering 2 new recipes.png                # Screenshot: Entering 2 new recipes and viewing results
```

### Running the Script

#### Run Exercise_1.3.py
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the script
python "Exercise 1.3/Exercise_1.3.py"
```

The script will:
1. Prompt you to enter how many recipes you'd like to add
2. For each recipe, collect:
   - Recipe name
   - Cooking time (in minutes)
   - Number of ingredients
   - Each ingredient name
3. Display all recipes with their details and calculated difficulty levels
4. Display all unique ingredients in alphabetical order

#### Run from IPython
```bash
# Activate virtual environment and launch IPython
source venv/bin/activate
ipython

# In IPython, run:
%run "Exercise 1.3/Exercise_1.3.py"
```

### Key Programming Concepts Demonstrated

- **Functions**: Creating reusable code blocks with `def` and return values
- **User Input**: Collecting and processing multiple inputs dynamically
- **Nested Loops**: Iterating through recipes and their ingredients
- **List Membership Testing**: Using `in` and `not in` operators to check for duplicates
- **Conditional Logic**: Multi-branch if-elif statements for difficulty calculation
- **List Operations**: Appending, sorting, and iterating through lists
- **Data Processing**: Building and maintaining data structures incrementally

### Notes

- The script uses functions to organize code and improve reusability
- Ingredients are automatically deduplicated when added to the master ingredients list
- Difficulty is calculated dynamically based on recipe attributes, not stored
- All ingredients are displayed in alphabetical order for better readability
- This exercise demonstrates practical application of functions, loops, and conditional logic in a real-world scenario

## Exercise 1.4: Recipe Storage and Search with File I/O

### Overview
This exercise extends the recipe management system by adding data storage using Python's `pickle` module. The exercise is divided into two scripts: one for inputting recipes and saving them to a binary file, and another for searching recipes by ingredient.

### What Was Accomplished

1. **Created `recipe_input.py`**: A script that collects recipes from users and stores them in a binary file
   - Implements `calc_difficulty()` function to calculate recipe difficulty
   - Implements `take_recipe()` function to collect recipe information from users
   - Handles file operations with try-except-else-finally blocks
   - Supports both creating new files and appending to existing files
   - Uses pickle to serialize and save data structures

2. **Created `recipe_search.py`**: A script that loads recipes from a binary file and allows searching by ingredient
   - Implements `display_recipe()` function to format and display recipe details
   - Implements `search_ingredient()` function to search for recipes containing a specific ingredient
   - Displays available ingredients with numbered options using `enumerate()`
   - Includes error handling for invalid user input and missing files

3. **File I/O Operations**: 
   - Learned to work with binary files using pickle module
   - Implemented proper exception handling for file operations
   - Created persistent data storage that survives between script executions

4. **Exception Handling**: 
   - Used try-except-else-finally blocks for robust error handling
   - Handled FileNotFoundError for new file creation
   - Implemented user input validation with error messages

### Project Structure

```
.
└── Exercise 1.4/
    ├── recipe_input.py                                    # Script for inputting and saving recipes
    ├── recipe_search.py                                   # Script for searching recipes by ingredient
    ├── learning_journal.md                                # Learning journal
    ├── Part 1 Step 1 - Activating venv.png               # Screenshot: Activating virtual environment
    ├── Part 1 Step 2 - Creating new file.png             # Screenshot: Creating new binary file
    ├── Part 1 Step 3 - Saving recipes.png                # Screenshot: Saving recipes to file
    ├── Part 1 Step 4 - Adding recipe to existing file.png # Screenshot: Adding recipes to existing file
    ├── Part 2 Step 1 - Running recipe search.png        # Screenshot: Running recipe search script
    ├── Part 2 Step 2 - Searching for recipes by ingredient.png # Screenshot: Searching for recipes
    └── Part 2 Step 3 - Search error handling.png        # Screenshot: Error handling demonstration
```

### Running the Scripts

#### Run recipe_input.py
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the script
python "Exercise 1.4/recipe_input.py"
```

The script will:
1. Prompt you to enter a filename for storing recipes (e.g., `my_recipes.bin`)
2. Attempt to load existing recipes from that file (or create new data if file doesn't exist)
3. Ask how many recipes you'd like to enter
4. Collect recipe information for each recipe (name, cooking time, ingredients)
5. Calculate difficulty for each recipe automatically
6. Save all recipes and ingredients to the binary file

#### Run recipe_search.py
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the script
python "Exercise 1.4/recipe_search.py"
```

The script will:
1. Prompt you to enter the filename containing your recipes
2. Load the recipes from the binary file
3. Display all available ingredients with numbers
4. Allow you to search for recipes containing a specific ingredient
5. Display all recipes that contain the selected ingredient

### Notes

- The pickle module allows you to save complex Python data structures (lists, dictionaries) to binary files
- Exception handling is crucial for file operations since files may not exist
- The try-except-else-finally structure ensures proper resource management
- Data structure consistency is important when loading and saving files
- The scripts can be run multiple times to add more recipes to existing files
- Error handling provides user-friendly messages when files are missing or input is invalid
- This exercise demonstrates real-world file persistence patterns used in many applications
