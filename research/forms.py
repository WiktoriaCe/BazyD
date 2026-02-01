from django import forms
from .models import CellLine, AnimalModel, Experiment


class CellLineForm(forms.ModelForm):
    class Meta:
        model = CellLine
        fields = ['name', 'cell_type', 'origin', 'tissue_type', 'description', 'passage_number']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class AnimalModelForm(forms.ModelForm):
    class Meta:
        model = AnimalModel
        fields = ['name', 'species', 'strain', 'genetic_background', 'age_weeks', 'sex', 'weight_grams', 'health_status', 'source']
        widgets = {
            'genetic_background': forms.Textarea(attrs={'rows': 3}),
        }


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['title', 'protocol', 'status', 'start_date', 'end_date', 'lab', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }