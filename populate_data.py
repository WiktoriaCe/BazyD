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
    researchers_data = [
        {'username': 'jan_kowalski', 'email': 'jan.kowalski@example.com', 'first_name': 'Jan', 'last_name': 'Kowalski'},
        {'username': 'anna_kowalska', 'email': 'anna.kowalska@example.com', 'first_name': 'Anna', 'last_name': 'Kowalska'},
        {'username': 'piotr_nowak', 'email': 'piotr.nowak@example.com', 'first_name': 'Piotr', 'last_name': 'Nowak'},
        {'username': 'maria_lewandowska', 'email': 'maria.lewandowska@example.com', 'first_name': 'Maria', 'last_name': 'Lewandowska'},
        {'username': 'jan_szymczak', 'email': 'jan.szymczak@example.com', 'first_name': 'Jan', 'last_name': 'Szymczak'},
        {'username': 'katarzyna_wilk', 'email': 'katarzyna.wilk@example.com', 'first_name': 'Katarzyna', 'last_name': 'Wilk'},
        {'username': 'rafal_michalski', 'email': 'rafal.michalski@example.com', 'first_name': 'Rafał', 'last_name': 'Michalski'},
        {'username': 'beata_walczak', 'email': 'beata.walczak@example.com', 'first_name': 'Beata', 'last_name': 'Walczak'},
        {'username': 'tomasz_sokolowski', 'email': 'tomasz.sokolowski@example.com', 'first_name': 'Tomasz', 'last_name': 'Sokołowski'},
        {'username': 'natalia_ostrowska', 'email': 'natalia.ostrowska@example.com', 'first_name': 'Natalia', 'last_name': 'Ostrowska'},
        {'username': 'sebastian_kucharski', 'email': 'sebastian.kucharski@example.com', 'first_name': 'Sebastian', 'last_name': 'Kucharski'},
    ]
    
    researchers = []
    for data in researchers_data:
        r, created = User.objects.get_or_create(
            username=data['username'],
            defaults={**data, 'password': 'password123'}
        )
        if created:  # Jeśli user nie istniał, ustaw hasło
            r.set_password('password123')
            r.save()
        researchers.append(r)
    researcher = researchers[0]  # Główny researcher do eksperymentów
    print(f"✓ Stworzone {len(researchers)} konta badaczy")
    
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
        {
            'name': 'A549',
            'cell_type': 'cancer',
            'origin': 'human',
            'tissue_type': 'epithelial',
            'passage_number': 120,
            'description': 'Human lung carcinoma cells'
        },
        {
            'name': 'U87',
            'cell_type': 'cancer',
            'origin': 'human',
            'tissue_type': 'glial',
            'passage_number': 95,
            'description': 'Human glioblastoma cells'
        },
        {
            'name': 'MDCK',
            'cell_type': 'normal',
            'origin': 'dog',
            'tissue_type': 'epithelial',
            'passage_number': 180,
            'description': 'Canine kidney epithelial cells'
        },
        {
            'name': 'Jurkat',
            'cell_type': 'cancer',
            'origin': 'human',
            'tissue_type': 'hematopoietic',
            'passage_number': 230,
            'description': 'Human T-cell leukemia cells'
        },
        {
            'name': 'HepG2',
            'cell_type': 'cancer',
            'origin': 'human',
            'tissue_type': 'hepatic',
            'passage_number': 130,
            'description': 'Human hepatocellular carcinoma cells'
        },
        {
            'name': 'NSC34',
            'cell_type': 'normal',
            'origin': 'mouse',
            'tissue_type': 'neuronal',
            'passage_number': 110,
            'description': 'Mouse motor neuron cells'
        },
        {
            'name': 'HT-29',
            'cell_type': 'cancer',
            'origin': 'human',
            'tissue_type': 'epithelial',
            'passage_number': 140,
            'description': 'Human colorectal adenocarcinoma cells'
        },
        {
            'name': 'Caco-2',
            'cell_type': 'cancer',
            'origin': 'human',
            'tissue_type': 'epithelial',
            'passage_number': 125,
            'description': 'Human colorectal carcinoma cells'
        },
        {
            'name': '3T3',
            'cell_type': 'normal',
            'origin': 'mouse',
            'tissue_type': 'fibroblast',
            'passage_number': 250,
            'description': 'Mouse embryonic fibroblasts'
        },
        {
            'name': 'PC-12',
            'cell_type': 'cancer',
            'origin': 'rat',
            'tissue_type': 'neuronal',
            'passage_number': 180,
            'description': 'Rat pheochromocytoma cells'
        },
        {
            'name': 'COS-7',
            'cell_type': 'normal',
            'origin': 'monkey',
            'tissue_type': 'fibroblast',
            'passage_number': 200,
            'description': 'African green monkey kidney fibroblasts'
        },
        {
            'name': 'BHK-21',
            'cell_type': 'normal',
            'origin': 'hamster',
            'tissue_type': 'fibroblast',
            'passage_number': 220,
            'description': 'Baby hamster kidney cells'
        },
        {
            'name': 'SF9',
            'cell_type': 'normal',
            'origin': 'insect',
            'tissue_type': 'ovarian',
            'passage_number': 300,
            'description': 'Spodoptera frugiperda ovarian cells'
        },
        {
            'name': 'Sf21',
            'cell_type': 'normal',
            'origin': 'insect',
            'tissue_type': 'ovarian',
            'passage_number': 280,
            'description': 'Spodoptera frugiperda cell line variant'
        },
    ]
    
    cell_lines = []
    for i, data in enumerate(cell_lines_data):
        # Przypisz każdą linię komórkową do innego użytkownika
        assigned_researcher = researchers[i % len(researchers)]
        cl, _ = CellLine.objects.get_or_create(
            name=data['name'],
            defaults={**data, 'created_by': assigned_researcher}
        )
        cell_lines.append(cl)
    print(f"✓ Stworzone {len(cell_lines)} linii komórkowych")
    
    # Stwórz modele zwierzęce
    animal_models_data = [
        {
            'name': 'Myszak C57BL/6',
            'species': 'mouse',
            'strain': 'C57BL/6',
            'age_weeks': 12,
            'sex': 'M',
            'weight_grams': 28.5,
            'health_status': 'healthy',
            'source': 'Charles River Labs'
        },
        {
            'name': 'Myszak BALB/c',
            'species': 'mouse',
            'strain': 'BALB/c',
            'age_weeks': 10,
            'sex': 'F',
            'weight_grams': 24.3,
            'health_status': 'healthy',
            'source': 'Charles River Labs'
        },
        {
            'name': 'Szczur Sprague Dawley',
            'species': 'rat',
            'strain': 'Sprague Dawley',
            'age_weeks': 16,
            'sex': 'M',
            'weight_grams': 350,
            'health_status': 'healthy',
            'source': 'Charles River Labs'
        },
        {
            'name': 'Myszak NOD/SCID',
            'species': 'mouse',
            'strain': 'NOD/SCID',
            'age_weeks': 8,
            'sex': 'F',
            'weight_grams': 22.1,
            'health_status': 'healthy',
            'source': 'Jackson Laboratory'
        },
        {
            'name': 'Myszak FVB/N',
            'species': 'mouse',
            'strain': 'FVB/N',
            'age_weeks': 14,
            'sex': 'M',
            'weight_grams': 27.8,
            'health_status': 'healthy',
            'source': 'Charles River Labs'
        },
        {
            'name': 'Szczur Lewis',
            'species': 'rat',
            'strain': 'Lewis',
            'age_weeks': 12,
            'sex': 'M',
            'weight_grams': 280,
            'health_status': 'healthy',
            'source': 'Charles River Labs'
        },
        {
            'name': 'Ryba AB',
            'species': 'zebrafish',
            'strain': 'AB',
            'age_weeks': 24,
            'sex': 'M',
            'weight_grams': 0.5,
            'health_status': 'healthy',
            'source': 'University Fish Facility'
        },
        {
            'name': 'Owsiuszek w1118',
            'species': 'drosophila',
            'strain': 'w1118',
            'age_weeks': 1,
            'sex': 'M',
            'weight_grams': 0.001,
            'health_status': 'healthy',
            'source': 'Bloomington Drosophila Stock Center'
        },
        {
            'name': 'Mysz 129/SvJ',
            'species': 'mouse',
            'strain': '129/SvJ',
            'age_weeks': 12,
            'sex': 'M',
            'weight_grams': 26.0,
            'health_status': 'healthy',
            'source': 'Jackson Laboratory'
        },
        {
            'name': 'Mysz DBA/2',
            'species': 'mouse',
            'strain': 'DBA/2',
            'age_weeks': 11,
            'sex': 'F',
            'weight_grams': 23.5,
            'health_status': 'healthy',
            'source': 'Charles River Labs'
        },
        {
            'name': 'Mysz outbred Swiss',
            'species': 'mouse',
            'strain': 'Outbred Swiss',
            'age_weeks': 9,
            'sex': 'M',
            'weight_grams': 28.5,
            'health_status': 'healthy',
            'source': 'Charles River Labs'
        },
        {
            'name': 'Szczur Fisher 344',
            'species': 'rat',
            'strain': 'Fisher 344',
            'age_weeks': 14,
            'sex': 'M',
            'weight_grams': 300,
            'health_status': 'healthy',
            'source': 'Charles River Labs'
        },
        {
            'name': 'Szczur Long-Evans',
            'species': 'rat',
            'strain': 'Long-Evans',
            'age_weeks': 13,
            'sex': 'F',
            'weight_grams': 280,
            'health_status': 'healthy',
            'source': 'Charles River Labs'
        },
        {
            'name': 'Ryba TL',
            'species': 'zebrafish',
            'strain': 'TL',
            'age_weeks': 20,
            'sex': 'M',
            'weight_grams': 0.5,
            'health_status': 'healthy',
            'source': 'University Fish Facility'
        },
        {
            'name': 'Ryba WIK',
            'species': 'zebrafish',
            'strain': 'WIK',
            'age_weeks': 22,
            'sex': 'F',
            'weight_grams': 0.55,
            'health_status': 'healthy',
            'source': 'University Fish Facility'
        },
    ]
    
    animal_models = []
    for i, data in enumerate(animal_models_data):
        # Przypisz każdy model zwierzęcy do innego użytkownika
        assigned_researcher = researchers[i % len(researchers)]
        am, _ = AnimalModel.objects.get_or_create(
            name=data['name'],
            defaults={**data, 'created_by': assigned_researcher}
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
        {
            'title': 'Flow Cytometry Analysis',
            'experiment_type': 'in_vitro',
            'objective': 'Determine cell surface markers and apoptosis',
            'methodology': 'Fluorescent antibody staining and FACS analysis',
            'description': 'Flow cytometry protocol for cell characterization'
        },
        {
            'title': 'Western Blotting Protocol',
            'experiment_type': 'in_vitro',
            'objective': 'Detect protein expression and modifications',
            'methodology': 'SDS-PAGE and immunodetection',
            'description': 'Standard Western blot protocol for protein analysis'
        },
        {
            'title': 'Immunohistochemistry Analysis',
            'experiment_type': 'in_vivo',
            'objective': 'Visualize protein localization in tissues',
            'methodology': 'Tissue sectioning, antibody staining, and imaging',
            'description': 'IHC protocol for tissue analysis'
        },
        {
            'title': 'Pharmacokinetics Study',
            'experiment_type': 'in_vivo',
            'objective': 'Measure drug absorption and distribution',
            'methodology': 'Plasma sampling and LC-MS/MS analysis',
            'description': 'PK protocol for drug disposition studies'
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
    
    # Stwórz eksperymenty - każdy z wyjątkowym zajęciem (linia komórkowa LUB model zwierzęcy)
    start_date = datetime.now().date() - timedelta(days=30)
    
    experiments_data = [
        {
            'title': 'Drug X Cytotoxicity Study - HeLa Cells',
            'protocol': protocols[0],
            'status': 'completed',
            'start_date': start_date,
            'end_date': start_date + timedelta(days=7),
            'principal_investigator': researchers[0],
            'lab': 'Lab A - Oncology',
            'cell_line': cell_lines[0],  # HeLa
            'animal_model': None,
        },
        {
            'title': 'Drug Y Efficacy in C57BL/6 Tumor Model',
            'protocol': protocols[1],
            'status': 'ongoing',
            'start_date': start_date + timedelta(days=14),
            'end_date': None,
            'principal_investigator': researchers[1],
            'lab': 'Lab B - In Vivo',
            'cell_line': None,
            'animal_model': animal_models[4],  # Myszak C57BL/6
        },
        {
            'title': 'Gene Expression Response to Treatment',
            'protocol': protocols[2],
            'status': 'ongoing',
            'start_date': start_date + timedelta(days=20),
            'end_date': None,
            'principal_investigator': researchers[2],
            'lab': 'Lab A - Oncology',
            'cell_line': cell_lines[1],  # A549
            'animal_model': None,
        },
        {
            'title': 'Flow Cytometry - Apoptosis Assessment',
            'protocol': protocols[3],
            'status': 'completed',
            'start_date': start_date - timedelta(days=15),
            'end_date': start_date - timedelta(days=10),
            'principal_investigator': researchers[3],
            'lab': 'Lab C - Flow Cytometry',
            'cell_line': cell_lines[2],  # MCF-7
            'animal_model': None,
        },
        {
            'title': 'Protein Expression in Drug-Treated Cells',
            'protocol': protocols[4],
            'status': 'ongoing',
            'start_date': start_date + timedelta(days=5),
            'end_date': None,
            'principal_investigator': researchers[4],
            'lab': 'Lab A - Oncology',
            'cell_line': cell_lines[3],  # CHO
            'animal_model': None,
        },
        {
            'title': 'Tumor Tissue Immunostaining Study',
            'protocol': protocols[5],
            'status': 'completed',
            'start_date': start_date - timedelta(days=20),
            'end_date': start_date - timedelta(days=12),
            'principal_investigator': researchers[5],
            'lab': 'Lab D - Pathology',
            'cell_line': None,
            'animal_model': animal_models[12],  # Szczur Lewis
        },
        {
            'title': 'Pharmacokinetic Profile - Drug A',
            'protocol': protocols[6],
            'status': 'ongoing',
            'start_date': start_date + timedelta(days=2),
            'end_date': None,
            'principal_investigator': researchers[6],
            'lab': 'Lab E - PK/PD',
            'cell_line': None,
            'animal_model': animal_models[13],  # Szczur Sprague Dawley
        },
        {
            'title': 'Long-term Toxicity Study in Rats',
            'protocol': protocols[1],
            'status': 'ongoing',
            'start_date': start_date - timedelta(days=30),
            'end_date': None,
            'principal_investigator': researchers[7],
            'lab': 'Lab B - In Vivo',
            'cell_line': None,
            'animal_model': animal_models[0],  # Mysz 129/SvJ
        },
    ]
    
    experiments = []
    experiments_spec = {}  # Przechowaj info czy eksperyment ma cell_line czy animal_model
    for data in experiments_data:
        cell_line = data.pop('cell_line')
        animal_model = data.pop('animal_model')
        exp, _ = Experiment.objects.get_or_create(
            title=data['title'],
            start_date=data['start_date'],
            defaults=data
        )
        experiments.append(exp)
        experiments_spec[exp.id] = {'cell_line': cell_line, 'animal_model': animal_model}
    print(f"✓ Stworzone {len(experiments)} eksperymenty")
    
    # Dodaj próbki DO WYBRANYCH eksperymentów (tylko te z cell_line)
    exp_samples_data = []
    for i, exp in enumerate(experiments):
        cell_line = experiments_spec[exp.id]['cell_line']
        if cell_line:  # Tylko dla eksperymentów z linią komórkową
            # Dodaj 3 próbki na eksperyment
            for treatment_num in range(3):
                exp_samples_data.append({
                    'experiment': exp,
                    'cell_line': cell_line,
                    'treatment': f'{cell_line.name} Treatment {treatment_num + 1}',
                    'concentration': (treatment_num + 1) * 5,
                    'duration_hours': 24
                })
    
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
    
    # Dodaj zwierzęta DO WYBRANYCH eksperymentów (tylko te z animal_model)
    exp_animals_data = []
    for i, exp in enumerate(experiments):
        animal_model = experiments_spec[exp.id]['animal_model']
        if animal_model:  # Tylko dla eksperymentów z modelem zwierzęcym
            # Dodaj 2 grupy zwierząt (Control i Treatment)
            exp_animals_data.append({
                'experiment': exp,
                'animal_model': animal_model,
                'treatment_group': 'Control',
                'number_of_animals': 5
            })
            exp_animals_data.append({
                'experiment': exp,
                'animal_model': animal_model,
                'treatment_group': 'Treatment',
                'number_of_animals': 5,
                'dosage': '10 mg/kg'
            })
    
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
    
    # Dodaj wyniki dla próbek
    results_data = []
    for i, sample in enumerate(samples[:6]):  # Dodaj wyniki dla pierwszych 6 próbek
        results_data.append({
            'experiment': sample.experiment,
            'parameter_name': 'cell_viability',
            'unit': '%',
            'method': 'MTT assay',
            'sample': sample,
            'value': max(100 - i * 10, 20)
        })
    
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
    for sample in samples[:6]:  # Dodaj geny dla pierwszych 6 próbek
        for gene in genes[:2]:
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
        {'experiment': experiments[0], 'title': 'Protocol Amendment', 'document_type': 'protocol_amendment', 'content': 'Standard MTT assay with HeLa cells - optimized for 24-hour assay'},
        {'experiment': experiments[1], 'title': 'In Vivo Report', 'document_type': 'results', 'content': 'Tumor growth inhibition study in C57BL/6 mice with drug Y'},
        {'experiment': experiments[2], 'title': 'Lab Notes', 'document_type': 'note', 'content': 'Gene expression data validated by qPCR analysis'},
    ]
    
    docs = []
    for data in docs_data:
        doc = Documentation.objects.create(
            **data,
            author=researcher
        )
        docs.append(doc)
    print(f"✓ Dodane {len(docs)} dokumenty")
    
    # Utwórz superużytkownika do panelu admina, jeśli nie istnieje
    if not User.objects.filter(username='researcher').exists():
        User.objects.create_superuser('researcher', 'researcher@example.com', 'password123')
        print("✓ Stworzono superużytkownika 'researcher' z hasłem 'password123'")
    else:
        print("✓ Superużytkownik 'researcher' już istnieje")
    
    print("\nWszystkie dane zostały stworzone pomyślnie!")
    print(f"\nPrzypomnienie: Zaloguj się na http://localhost:8000/admin/")
    print(f"Użytkownik: researcher | Hasło: password123")


if __name__ == '__main__':
    create_sample_data()