from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipes_home, name='recipes_home'),
    path('recipes/', views.recipes_list, name='recipes_list'),
    path('recipes/search/', views.recipe_search, name='recipe_search'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
]

