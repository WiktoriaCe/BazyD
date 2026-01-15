"""
Script do generowania przykładowych danych dla testów i demonstracji
"""

import os
import django
from datetime import datetime, timedelta
from random import randint, choice, uniform

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world.settings')
django.setup()

from django.contrib.auth.models import User
from research.models import (
    CellLine, AnimalModel, ResearchProtocol, Experiment,
    ExperimentSample, ExperimentAnimal, Result, GeneExpression, Documentation
)


def create_sample_data():
    """Stwórz przykładowe dane"""
    
    print("Tworzenie przykładowych danych...")
    
    # Stwórz użytkowników
    if not User.objects.filter(username='researcher').exists():
        researcher = User.objects.create_user(
            username='researcher',
            email='researcher@example.com',
            password='password123',
            first_name='John',
            last_name='Smith'
        )
    else:
        researcher = User.objects.get(username='researcher')
    
    # Stwórz linie komórkowe
    cell_lines_data = [
        {
            'name': 'HeLa',
            'cell_type': 'cancer',
            'origin': 'human',
            'tissue_type': 'epithelial',
            'passage_number': 150,
            'description': 'Human cervical cancer cells'
        },
        {
            'name': 'HEK293',
            'cell_type': 'normal',
            'origin': 'human',
            'tissue_type': 'embryonic',
            'passage_number': 45,
            'description': 'Human embryonic kidney cells'
        },
        {
            'name': 'MCF-7',
            'cell_type': 'cancer',
            'origin': 'human',
            'tissue_type': 'epithelial',
            'passage_number': 100,
            'description': 'Human breast cancer cells'
        },
        {
            'name': 'CHO',
            'cell_type': 'normal',
            'origin': 'hamster',
            'tissue_type': 'ovarian',
            'passage_number': 200,
            'description': 'Chinese hamster ovary cells'
        },
    ]
    
    cell_lines = []
    for data in cell_lines_data:
        cl, _ = CellLine.objects.get_or_create(
            name=data['name'],
            defaults={**data, 'created_by': researcher}
        )
        cell_lines.append(cl)
    print(f"✓ Stworzone {len(cell_lines)} linii komórkowych")
    
    # Stwórz modele zwierzęce
    animal_models_data = [
        {
            'name': 'C57BL/6-Mouse-001',
            'species': 'mouse',
            'strain': 'C57BL/6',
            'age_weeks': 12,
            'sex': 'M',
            'weight_grams': 28.5,
            'health_status': 'healthy',
            'source': 'Charles River Labs'
        },
        {
            'name': 'BALB/c-Mouse-001',
            'species': 'mouse',
            'strain': 'BALB/c',
            'age_weeks': 10,
            'sex': 'F',
            'weight_grams': 24.3,
            'health_status': 'healthy',
            'source': 'Charles River Labs'
        },
        {
            'name': 'Sprague-Dawley-Rat-001',
            'species': 'rat',
            'strain': 'Sprague Dawley',
            'age_weeks': 16,
            'sex': 'M',
            'weight_grams': 350,
            'health_status': 'healthy',
            'source': 'Charles River Labs'
        },
    ]
    
    animal_models = []
    for data in animal_models_data:
        am, _ = AnimalModel.objects.get_or_create(
            name=data['name'],
            defaults={**data, 'created_by': researcher}
        )
        animal_models.append(am)
    print(f"✓ Stworzone {len(animal_models)} modele zwierzęce")
    
    # Stwórz protokoły badań
    protocols_data = [
        {
            'title': 'MTT Assay Protocol for Cell Viability',
            'experiment_type': 'in_vitro',
            'objective': 'Determine cell viability after drug exposure',
            'methodology': 'Colorimetric assay measuring metabolic activity',
            'description': 'Standard MTT assay protocol for cytotoxicity testing'
        },
        {
            'title': 'Tumor Growth Inhibition Study',
            'experiment_type': 'in_vivo',
            'objective': 'Evaluate drug efficacy in tumor models',
            'methodology': 'Xenograft model with periodic tumor measurements',
            'description': 'In vivo efficacy testing protocol'
        },
        {
            'title': 'Gene Expression Analysis by qPCR',
            'experiment_type': 'in_vitro',
            'objective': 'Quantify mRNA expression levels',
            'methodology': 'Real-time qPCR with GAPDH normalization',
            'description': 'qPCR protocol for gene expression analysis'
        },
    ]
    
    protocols = []
    for data in protocols_data:
        p, _ = ResearchProtocol.objects.get_or_create(
            title=data['title'],
            defaults={**data, 'created_by': researcher}
        )
        protocols.append(p)
    print(f"✓ Stworzone {len(protocols)} protokoły")
    
    # Stwórz eksperymenty
    start_date = datetime.now().date() - timedelta(days=30)
    
    experiments_data = [
        {
            'title': 'Drug X Cytotoxicity Study - HeLa Cells',
            'protocol': protocols[0],
            'status': 'completed',
            'start_date': start_date,
            'end_date': start_date + timedelta(days=7),
            'principal_investigator': researcher,
            'lab': 'Lab A - Oncology',
        },
        {
            'title': 'Drug Y Efficacy in C57BL/6 Tumor Model',
            'protocol': protocols[1],
            'status': 'ongoing',
            'start_date': start_date + timedelta(days=14),
            'end_date': None,
            'principal_investigator': researcher,
            'lab': 'Lab B - In Vivo',
        },
        {
            'title': 'Gene Expression Response to Treatment',
            'protocol': protocols[2],
            'status': 'ongoing',
            'start_date': start_date + timedelta(days=20),
            'end_date': None,
            'principal_investigator': researcher,
            'lab': 'Lab A - Oncology',
        },
    ]
    
    experiments = []
    for data in experiments_data:
        exp, _ = Experiment.objects.get_or_create(
            title=data['title'],
            start_date=data['start_date'],
            defaults=data
        )
        experiments.append(exp)
    print(f"✓ Stworzone {len(experiments)} eksperymenty")
    
    # Dodaj próbki do eksperymentu
    exp_samples_data = [
        {'experiment': experiments[0], 'cell_line': cell_lines[0], 'treatment': 'Control', 'concentration': 0, 'duration_hours': 24},
        {'experiment': experiments[0], 'cell_line': cell_lines[0], 'treatment': 'Drug X', 'concentration': 1, 'duration_hours': 24},
        {'experiment': experiments[0], 'cell_line': cell_lines[0], 'treatment': 'Drug X', 'concentration': 10, 'duration_hours': 24},
        {'experiment': experiments[0], 'cell_line': cell_lines[0], 'treatment': 'Drug X', 'concentration': 100, 'duration_hours': 24},
        
        {'experiment': experiments[2], 'cell_line': cell_lines[1], 'treatment': 'Control', 'concentration': 0, 'duration_hours': 6},
        {'experiment': experiments[2], 'cell_line': cell_lines[1], 'treatment': 'Drug Y', 'concentration': 5, 'duration_hours': 6},
    ]
    
    samples = []
    for data in exp_samples_data:
        sample, _ = ExperimentSample.objects.get_or_create(
            experiment=data['experiment'],
            cell_line=data['cell_line'],
            treatment=data['treatment'],
            concentration=data['concentration'],
            defaults={'concentration_unit': 'µM', 'duration_hours': data['duration_hours'], 'replicate_number': 3}
        )
        samples.append(sample)
    print(f"✓ Dodane {len(samples)} próbki in vitro")
    
    # Dodaj zwierzęta do eksperymentu
    exp_animals_data = [
        {'experiment': experiments[1], 'animal_model': animal_models[0], 'treatment_group': 'Control', 'number_of_animals': 5},
        {'experiment': experiments[1], 'animal_model': animal_models[0], 'treatment_group': 'Drug Y 10mg/kg', 'number_of_animals': 5, 'dosage': '10 mg/kg'},
    ]
    
    exp_animals = []
    for data in exp_animals_data:
        ea, _ = ExperimentAnimal.objects.get_or_create(
            experiment=data['experiment'],
            animal_model=data['animal_model'],
            treatment_group=data['treatment_group'],
            defaults={'number_of_animals': data['number_of_animals'], 'dosage': data.get('dosage', ''), 'route_of_administration': 'IP'}
        )
        exp_animals.append(ea)
    print(f"✓ Dodane {len(exp_animals)} grupy zwierząt")
    
    # Dodaj wyniki
    results_data = [
        {'experiment': experiments[0], 'parameter_name': 'cell_viability', 'unit': '%', 'method': 'MTT assay', 'sample': samples[1], 'value': 95},
        {'experiment': experiments[0], 'parameter_name': 'cell_viability', 'unit': '%', 'method': 'MTT assay', 'sample': samples[2], 'value': 75},
        {'experiment': experiments[0], 'parameter_name': 'cell_viability', 'unit': '%', 'method': 'MTT assay', 'sample': samples[3], 'value': 45},
        {'experiment': experiments[0], 'parameter_name': 'cell_viability', 'unit': '%', 'method': 'MTT assay', 'sample': samples[0], 'value': 100},
    ]
    
    results = []
    for i, data in enumerate(results_data):
        result = Result.objects.create(
            **data,
            measurement_date=datetime.now() - timedelta(hours=i)
        )
        results.append(result)
    print(f"✓ Dodane {len(results)} wyniki")
    
    # Dodaj ekspresję genów
    genes = ['BRCA1', 'TP53', 'EGFR', 'HER2', 'MYC', 'GAPDH']
    
    gene_expressions = []
    for sample in samples[:4]:
        for gene in genes[:3]:
            ge = GeneExpression.objects.create(
                gene_name=gene,
                gene_id=f'ENSG{randint(100000000, 999999999)}',
                sample=sample,
                expression_level=round(uniform(0.1, 5.0), 2),
                measurement_method='qpcr',
                reference_gene='GAPDH',
                p_value=round(uniform(0.001, 0.05), 4)
            )
            gene_expressions.append(ge)
    print(f"✓ Dodane {len(gene_expressions)} pomiary ekspresji genów")
    
    # Dodaj dokumentację
    docs_data = [
        {'experiment': experiments[0], 'title': 'Protocol Amendment', 'document_type': 'protocol_amendment', 'content': 'Increased cell density for better toxicity detection'},
        {'experiment': experiments[1], 'title': 'Incident Report', 'document_type': 'incident_report', 'content': 'One animal showed unexpected weight loss on day 5'},
        {'experiment': experiments[2], 'title': 'Lab Notes', 'document_type': 'note', 'content': 'RNA quality was excellent (RIN > 8.0) for all samples'},
    ]
    
    docs = []
    for data in docs_data:
        doc = Documentation.objects.create(
            **data,
            author=researcher
        )
        docs.append(doc)
    print(f"✓ Dodane {len(docs)} dokumenty")
    
    print("\n✅ Wszystkie dane zostały stworzone pomyślnie!")
    print(f"\nPrzypomnienie: Zaloguj się na http://localhost:8000/admin/")
    print(f"Użytkownik: researcher | Hasło: password123")


if __name__ == '__main__':
    create_sample_data()
