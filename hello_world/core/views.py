from django.shortcuts import render
from research.models import CellLine, AnimalModel, Experiment, Documentation
from django.contrib.auth.models import User

def index(request):
    # Pobierz wszystkie dane z modeli
    cell_lines = CellLine.objects.all()
    animal_models = AnimalModel.objects.all()
    experiments = Experiment.objects.all()
    users = User.objects.all()
    docs = Documentation.objects.all()
    
    context = {
        "title": "Medical Research Database",
        "cell_lines": cell_lines,
        "animal_models": animal_models,
        "experiments": experiments,
        "users": users,
        "docs": docs,
    }
    return render(request, "landing.html", context)
