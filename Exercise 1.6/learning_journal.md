# Exercise 1.6: Recipe Management with MySQL Database - Learning Journal

## Date: 12.04.2025

## What I Learned

### Database Connectivity
- **MySQL Connector**: Learned to use `mysql.connector` module to connect Python applications to MySQL databases
- **Connection Objects**: Created connection objects using `mysql.connector.connect()` with host, user, and password parameters
- **Cursor Objects**: Used cursor objects to execute SQL queries and fetch results from the database
- **Connection Management**: Understood the importance of properly closing connections and cursors to free up resources

### SQL Database Operations
- **CREATE DATABASE**: Learned to create databases using `CREATE DATABASE IF NOT EXISTS` to avoid errors from duplicate databases
- **USE Statement**: Used `USE` statement to select the active database for operations
- **CREATE TABLE**: Created tables with specific column types (INT, VARCHAR, AUTO_INCREMENT, PRIMARY KEY)
- **INSERT INTO**: Inserted new records into database tables using parameterized queries
- **SELECT**: Retrieved data from tables using SELECT statements with WHERE and LIKE clauses
- **UPDATE**: Modified existing records in the database using UPDATE statements
- **DELETE**: Removed records from the database using DELETE statements with WHERE clauses

### Data Type Handling
- **String vs List Conversion**: Learned to convert between Python lists and comma-separated strings for MySQL storage
  - `join()` method: Convert list to string (e.g., `", ".join(ingredients)`)
  - `split()` method: Convert string back to list (e.g., `ingredients_str.split(",")`)
- **MySQL Limitations**: Understood that MySQL doesn't fully support array data types, requiring string conversion for list data

### SQL Query Patterns
- **Parameterized Queries**: Used parameterized queries with `%s` placeholders to prevent SQL injection
- **LIKE Operator**: Used `LIKE` with wildcard `%` to search for patterns within strings (e.g., `%ingredient%`)
- **WHERE Clauses**: Filtered database results using WHERE clauses with various conditions
- **AUTO_INCREMENT**: Used AUTO_INCREMENT for primary keys to automatically generate unique IDs

### Menu-Driven Interfaces
- **While Loops**: Implemented continuous menu loops using `while True` to keep the program running
- **User Input Handling**: Created interactive menus that accept user choices and call appropriate functions
- **Exit Conditions**: Implemented exit mechanisms (e.g., typing 'quit') to break out of menu loops
- **Function Calls from Menus**: Learned to call different functions based on user menu selections

### Data Consistency
- **Automatic Recalculation**: Learned to automatically recalculate dependent fields (like difficulty) when related fields are updated
- **Transaction Management**: Used `conn.commit()` to save changes to the database after modifications
- **Data Integrity**: Ensured data consistency by updating related fields when primary fields change

## Challenges Faced

- Understanding how to convert between Python lists and comma-separated strings for MySQL storage
- Learning SQL syntax and query structure (INSERT, SELECT, UPDATE, DELETE)
- Implementing proper error handling for database operations
- Managing database connections and ensuring they're properly closed
- Understanding when to use LIKE with wildcards versus exact matches
- Handling the recalculation of difficulty when cooking_time or ingredients are updated
- Creating a user-friendly menu system that loops continuously until exit

## Solutions Found

- Used `", ".join(ingredients)` to convert lists to comma-separated strings for storage
- Used `ingredients_str.split(",")` with `strip()` to convert strings back to lists
- Implemented parameterized queries with `%s` placeholders for safe SQL execution
- Used `LIKE %ingredient%` pattern to search for ingredients anywhere in the ingredients string
- Created a `calculate_difficulty()` function that's called when cooking_time or ingredients change
- Used `while True` loop with break condition for the main menu
- Implemented try-except blocks around all database operations
- Ensured connections are closed in finally blocks or at program exit

## Reflection

- Database integration allows for persistent, structured data storage that endures throughout program restarts
- SQL provides a strong and standardized way to query and manipulate data
- Converting between data types (lists to strings) is necessary when working with databases that don't support all Python data types
- CRUD operations form the foundation of most database applications
- Error handling is crucial when working with external systems like databases
- Automatic recalculation of dependent fields maintains data consistency