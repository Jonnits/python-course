# Recipe Application

A Django web application for managing, searching, and sharing recipes. This application provides a complete recipe management system with user authentication, favorites, search functionality, and data visualization.

## Features

### Recipe Management
- **Browse Recipes**: View all available recipes in an attractive card-based layout
- **Recipe Details**: View detailed information including ingredients, cooking time, difficulty level, and descriptions
- **Add Recipes**: Logged-in users can add new recipes with images, ingredients, and descriptions
- **Search Recipes**: Advanced search functionality with filters for:
  - Recipe name (partial/wildcard matching)
  - Ingredients
  - Maximum cooking time
  - Difficulty level (Easy, Medium, Intermediate, Hard)
  - Author
- **Show All**: Option to view all recipes without filters

### User Features
- **User Authentication**: Secure login and registration system
- **User Registration**: Custom registration form with password validation:
  - 8-16 characters
  - At least 1 number
  - At least 1 uppercase letter
- **Favorites**: Users can favorite recipes and view their favorites collection
- **User Profile**: View favorite recipes and manage profile
- **Profile Management**: Delete profile with confirmation

### Data Visualization
- **Bar Chart**: Recipes by difficulty level
- **Pie Chart**: Recipes by author
- **Line Chart**: Average cooking time by difficulty level

### Technical Features
- **Automatic Difficulty Calculation**: Recipes automatically calculate difficulty based on cooking time and number of ingredients
- **Image Support**: Recipes can include images
- **Responsive Design**: Modern, clean UI with custom styling using Lora font
- **Protected Views**: Recipe details require authentication

## Technology Stack

- **Backend**: Django 4.2.27
- **Database**: SQLite (development), PostgreSQL (production on Heroku)
- **Data Analysis**: pandas, matplotlib
- **Image Processing**: Pillow
- **Web Server**: Gunicorn (production)
- **Static Files**: WhiteNoise

## Project Structure

```
src/
├── manage.py
├── Procfile              # Heroku deployment configuration
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
├── recipe_project/      # Main Django project
│   ├── settings.py     # Project settings
│   ├── urls.py         # URL configuration
│   ├── views.py        # Authentication views
│   └── forms.py        # Registration form
├── recipes/            # Recipes app
│   ├── models.py       # Recipe model
│   ├── views.py        # Recipe views
│   ├── forms.py        # Recipe forms
│   ├── urls.py         # Recipe URLs
│   ├── templates/     # Recipe templates
│   └── tests.py        # Recipe tests
├── users/              # Users app
│   ├── models.py       # UserProfile model
│   └── admin.py        # User admin
├── ingredients/        # Ingredients app
├── templates/          # Project-level templates
└── media/             # User-uploaded files
```

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Jonnits/django-recipe-application.git
   cd django-recipe-application
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Homepage: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Environment Variables

For production deployment, set the following environment variables:

- `DJANGO_SECRET_KEY`: Django secret key (required for production)
- `DEBUG`: Set to `False` for production
- `DATABASE_URL`: Automatically set by Heroku for PostgreSQL

## Deployment

This application is configured for deployment on Heroku. See the deployment instructions in the project documentation.

## Testing

Run the test suite with:
```bash
python manage.py test recipes -v 2
```

The test suite includes:
- Model tests (difficulty calculation, ingredients sorting)
- View tests (authentication, search, favorites)
- Form tests (validation, user registration)
- URL tests

## Security Notes

- **SECRET_KEY**: The `SECRET_KEY` in `settings.py` uses environment variables (`os.environ.get('DJANGO_SECRET_KEY', ...)`). 
  - The fallback key in the code is **only for local development**
  - **For production on Heroku**, set `DJANGO_SECRET_KEY` via Heroku config variables (see deployment instructions)
  - The fallback key will NOT be used in production if `DJANGO_SECRET_KEY` is set
- **DEBUG**: Set to `False` in production via environment variable (`DEBUG=False` on Heroku)
- **Database**: Uses SQLite locally, PostgreSQL on Heroku (automatically configured via `DATABASE_URL`)
- **Static Files**: Served via WhiteNoise in production
- **settings.py**: The file is tracked in git but uses environment variables for sensitive data. This is safe as long as production environment variables are properly set.

## Contributing

This is a learning project. Feel free to explore the code and adapt it for your own use.

## Author

A Jon Rubra app - https://www.jonrubra.com/
