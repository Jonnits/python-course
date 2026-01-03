# Exercise 1.3: Recipe Management with Difficulty Calculation - Learning Journal

## Date: 12.02.2025

## What I Learned

### Functions
- **Function Definition**: Learned how to define functions using `def` to encapsulate reusable code blocks
- **Function Return Values**: Understood how functions can return data (in this case, a dictionary) to be used by the calling code
- **User Input in Functions**: Practiced collecting user input within functions to build data structures dynamically

### Control Flow
- **For Loops**: Gained experience with nested for loops to iterate through lists and process data
- **Conditional Statements**: Learned to use `if` statements with the `in` and `not in` operators to check for element membership in lists
- **Complex Conditionals**: Practiced using multiple conditions with `and` operators to determine recipe difficulty levels

### List Operations
- **List Membership Testing**: Used the `in` keyword to check if an element exists in a list before adding it
- **List Sorting**: Learned to use `sorted()` function to display ingredients in alphabetical order
- **Dynamic List Building**: Built lists incrementally by appending elements conditionally

### Data Processing
- **Unique Element Collection**: Implemented logic to collect unique ingredients across multiple recipes
- **Difficulty Calculation**: Created a multi-condition algorithm to calculate recipe difficulty based on cooking time and ingredient count
- **Data Display**: Formatted and displayed structured data with proper formatting and organization

## Challenges Faced

- Understanding how to check for element membership in lists using the `in` operator
- Implementing nested loops correctly to iterate through recipe ingredients
- Setting up the difficulty calculation logic with multiple conditional branches
- Ensuring ingredients are only added once to the ingredients_list (avoiding duplicates)

## Solutions Found

- Used `if ingredient not in ingredients_list:` to check for duplicates before appending
- Structured nested loops carefully: outer loop for recipes, inner loop for ingredients within each recipe
- Created a clear if-elif-elif-elif structure for difficulty calculation covering all four cases
- Used `sorted()` function to alphabetize the final ingredients list display

## Reflection

- Functions help organize code and make it more reusable and maintainable
- Nested loops are powerful for processing nested data structures (lists within dictionaries)
- Conditional logic requires careful consideration of all possible cases
- The `in` and `not in` operators are essential for membership testing in Python
- Sorting data before display improves user experience and readability
- Building data structures incrementally (collecting recipes and ingredients) is a common pattern in programming

