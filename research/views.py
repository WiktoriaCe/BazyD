"""
Views for frontend forms and helpers.
API viewsets were removed; these views provide simple form-based creation
for CellLine, AnimalModel and Experiment (protected to logged-in users).
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CellLineForm, AnimalModelForm, ExperimentForm


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
