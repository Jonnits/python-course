# Task 2.5 - Model Review and Updates

## Current Models (from Exercise 2.3)

### 1. Recipe Model (recipes app)
**Current attributes:**
- `name` (CharField, max_length=120)
- `recipe_id` (IntegerField, primary_key=True, editable=False)
- `author` (ForeignKey to User)
- `cooking_time` (IntegerField)
- `ingredients` (TextField)
- `description` (TextField)
- `difficulty` (CharField, max_length=20)

**Issues identified:**
- `recipe_id` is set as primary_key with editable=False, which means it won't auto-increment. I have since learned that Django typically uses an auto-incrementing `id` field as primary key.
- `difficulty` is stored but should be calculated dynamically (based on cooking_time and number of ingredients), per this task's instructions.

**Proposed changes:**
- Remove `recipe_id` field and let Django use default auto-incrementing `id` field.
- Keep `difficulty` field for now (can be calculated and stored, or calculated on-the-fly in views).
- Adding `pic` field to store recipe images, per task instructions.

### 2. Ingredient Model (ingredients app)
**Current attributes:**
- `name` (CharField, max_length=100)
- `quantity` (CharField, max_length=50)

**Status:** No changes needed

### 3. UserProfile Model (users app)
**Current attributes:**
- `user` (OneToOneField to User)
- `name` (CharField, max_length=100)
- `email_address` (EmailField)
- `favorited_recipes` (ManyToManyField to Recipe)
- `submitted_recipes` (ManyToManyField to Recipe)

**Status:** No changes needed

## Decision

**Will update Recipe model:**
- Remove `recipe_id` field (use Django's default `id` field instead).
- Keep `difficulty` field (will calculate it when saving recipes).
- Add `pic` field to store recipe images.

