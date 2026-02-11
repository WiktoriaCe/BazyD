from django.shortcuts import render
from research.models import CellLine, AnimalModel, Experiment
from django.contrib.auth.models import User

def index(request):
    # Pobierz wszystkie dane z modeli. Szukany tekst będzie podświetlany w szablonie.
    q = request.GET.get('q', '').strip()

    # Zwracamy wszystkie wpisy; filtrowanie nie będzie usuwać pozostałych elementów
    cell_lines = CellLine.objects.all()

    animal_models = AnimalModel.objects.all()
    experiments = Experiment.objects.select_related('principal_investigator', 'protocol')
    experiments = experiments.prefetch_related('experiment_samples__cell_line', 'experiment_animals__animal_model').all()
    users = User.objects.all()
    
    context = {
        "title": "Medical Research Database",
        "cell_lines": cell_lines,
        "animal_models": animal_models,
        "experiments": experiments,
        "users": users,
        "q": q,
    }
    return render(request, "landing.html", context)
