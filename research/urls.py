"""
Frontend form routes for creating objects via the site.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('cell-line/', views.add_cell_line, name='add_cell_line'),
    path('animal-model/', views.add_animal_model, name='add_animal_model'),
    path('experiment/', views.add_experiment, name='add_experiment'),
]
