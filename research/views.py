"""
Views for frontend forms and helpers.
API viewsets were removed; these views provide simple form-based creation
for CellLine, AnimalModel and Experiment (protected to logged-in users).
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import CellLineForm, AnimalModelForm, ExperimentForm
from .models import Experiment
from django.shortcuts import get_object_or_404


def placeholder(request):
    # keeps landing render available if needed
    return render(request, "landing.html")


@login_required
def add_cell_line(request):
    if request.method == 'POST':
        form = CellLineForm(request.POST)
        if form.is_valid():
            cell_line = form.save(commit=False)
            cell_line.created_by = request.user
            cell_line.save()
            messages.success(request, f"Linia komórkowa '{cell_line.name}' została dodana.")
            return redirect('/')
    else:
        form = CellLineForm()
    return render(request, 'research/add_cell_line.html', {'form': form})


@login_required
def add_animal_model(request):
    if request.method == 'POST':
        form = AnimalModelForm(request.POST)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.created_by = request.user
            animal.save()
            messages.success(request, f"Model zwierzęcy '{animal.name}' został dodany.")
            return redirect('/')
    else:
        form = AnimalModelForm()
    return render(request, 'research/add_animal_model.html', {'form': form})


@login_required
def add_experiment(request):
    if request.method == 'POST':
        form = ExperimentForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            # ustaw aktualnego usera jako głównego badacza domyślnie
            exp.principal_investigator = request.user
            exp.save()
            messages.success(request, f"Eksperyment '{exp.title}' został dodany.")
            return redirect('/')
    else:
        form = ExperimentForm()
    return render(request, 'research/add_experiment.html', {'form': form})


def experiment_list(request):
    experiments = Experiment.objects.select_related('principal_investigator', 'protocol')
    experiments = experiments.prefetch_related('experiment_samples__cell_line', 'experiment_animals__animal_model').all().order_by('-start_date')
    return render(request, 'research/experiment_list.html', {'experiments': experiments})


def experiment_detail(request, pk):
    exp = get_object_or_404(Experiment, pk=pk)
    # prefetch related through objects
    samples = exp.experiment_samples.select_related('cell_line').all()
    animals = exp.experiment_animals.select_related('animal_model').all()
    results = exp.results.all().order_by('-measurement_date')
    return render(request, 'research/experiment_detail.html', {
        'experiment': exp,
        'samples': samples,
        'animals': animals,
        'results': results,
    })


def person_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # objects the user created or is PI of
    cell_lines = user.cell_lines.all()
    animal_models = user.animal_models.all()
    experiments = Experiment.objects.filter(principal_investigator=user).select_related('protocol')
    return render(request, 'research/person_detail.html', {
        'person': user,
        'cell_lines': cell_lines,
        'animal_models': animal_models,
        'experiments': experiments,
    })
