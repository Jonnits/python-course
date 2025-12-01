# Python Course

This repository contains my work for the Python specialization course, organized by exercise.

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
3. **Added 5 recipes**: Created recipe_1 through recipe_5 and added them to all_recipes
4. **Printed ingredients**: Displayed the ingredients list for each recipe as separate lists

### Project Structure

```
.
└── Exercise 1.2/
    ├── README.md              # Exercise documentation
    ├── learning_journal.md    # Learning journal
    ├── Step 1.png            # Screenshot: Creating recipe_1
    ├── Step 2.png            # Screenshot: Creating all_recipes
    ├── Step 3.png            # Screenshot: Adding 4 more recipes
    └── Step 4.png            # Screenshot: Printing ingredients
```

### Data Structure Choices

**For recipe_1 (individual recipe structure):**
I chose to use a dictionary for storing individual recipe information because it provides key-value pairs that allow for named, semantic access to recipe attributes. Unlike tuples or lists, dictionaries enable accessing data by meaningful keys (e.g., `recipe_1['name']`) rather than positional indices, which makes the code more readable and maintainable. Dictionaries also offer flexibility for future modifications, such as adding new recipe attributes without restructuring the entire data model.

**For all_recipes (outer structure):**
I chose to use a list for storing multiple recipes because it provides sequential storage with the ability to append, modify, and iterate through recipes easily. Lists maintain insertion order and allow for dynamic growth as new recipes are added. This sequential nature makes it straightforward to access recipes by index, iterate through all recipes, and perform operations like printing ingredients for each recipe in the collection.

