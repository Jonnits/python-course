# Exercise 1.5: Recipe Management using Object-Oriented Programming - Learning Journal

## Date: 12.03.2025

## What I Learned

### Object-Oriented Programming (OOP)
- **Classes**: Learned how to define classes to create custom data types that encapsulate both data (attributes) and behavior (methods)
- **Class vs Instance**: Understood the difference between class variables (shared across all instances) and instance variables (unique to each object)
- **Initialization**: Learned to use `__init__()` method to initialize objects with default or provided values
- **Encapsulation**: Practiced bundling data and methods together within a class to create self-contained objects

### Class Attributes and Methods
- **Instance Attributes**: Created attributes (name, ingredients, cooking_time, difficulty) that belong to each recipe object
- **Class Variables**: Used `all_ingredients` as a class variable to track ingredients across all recipe instances
- **Getter and Setter Methods**: Implemented methods to access and modify object attributes, following encapsulation principles
- **Instance Methods**: Created methods that operate on individual recipe objects (e.g., `add_ingredients()`, `search_ingredient()`)

### Special Methods
- **`__str__()` Method**: Learned to override the string representation method to customize how objects are displayed when printed
- **String Formatting**: Practiced creating well-formatted output for object display

### Method Design
- **Method Chaining**: Understood how methods can call other methods (e.g., `add_ingredients()` calls `update_all_ingredients()`)

### Search Functionality
- **Standalone Functions**: Created `recipe_search()` as a standalone function (not a method) that operates on lists of objects
- **Method Calls from Functions**: Learned to call instance methods from within standalone functions
- **Iteration Over Objects**: Practiced iterating through lists of objects and calling their methods

## Challenges Faced

- Understanding the difference between class variables and instance variables, and when to use each
- Knowing when to use getter/setter methods versus direct attribute access
- Deciding whether methods should be instance methods or standalone functions
- Ensuring class variables are updated correctly when new instances are created
- Understanding when `calculate_difficulty()` should be called (lazy evaluation in getter)

## Solutions Found

- Used class variable `all_ingredients` to track ingredients across all recipes, accessed via `Recipe.all_ingredients`
- Implemented getter/setter methods for name and cooking_time to follow encapsulation principles
- Used `*ingredients` in `add_ingredients()` to accept any number of ingredient arguments
- Made `recipe_search()` a standalone function since it operates on collections of objects, not individual objects
- Called `update_all_ingredients()` from within `add_ingredients()` to automatically maintain the class variable

## Reflection

- Object-Oriented Programming provides a natural way to model real-world entities (like recipes) with both data and behavior
- Classes help organize code by grouping related functionality together
- Encapsulation (using getters/setters) provides control over how attributes are accessed and modified
- Class variables are powerful for maintaining shared state across multiple instances
- The `__str__()` method makes objects more user-friendly by providing readable string representations
- Method chaining allows for smooth, cohesive code where methods call other methods to accomplish complex tasks
- OOP promotes code reusability and maintainability by organizing code into logical units

