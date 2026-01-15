# Medical Research Database - In Vitro/In Vivo Documentation System

System zarządzania badaniami in vitro / in vivo z obsługą linii komórkowych, modeli zwierzęcych, wyników eksperymentów i ekspresji genów.

## Technologia

- **Backend**: Django 5.2 + Django REST Framework
- **Baza danych**: SQLite (development) / PostgreSQL (production)
- **API**: RESTful API z Django REST Framework
- **Filtrowanie**: django-filter
- **CORS**: django-cors-headers

## Struktura projektu

```
research/
├── models.py          # Modele bazy danych
├── serializers.py     # DRF Serializers
├── views.py          # ViewSets dla API
├── admin.py          # Django Admin
├── urls.py           # API Routes
└── migrations/       # Migracje bazy danych
```

## Modele danych

### 1. **CellLine** - Linie komórkowe
- Nazwa, typ (cancer, normal, primary, stem)
- Pochodzenie, typ tkanki
- Numer pasażu
- Utworzone przez użytkownika

### 2. **AnimalModel** - Modele zwierzęce
- Gatunek (mysz, szczur, zebrafish, drosophila)
- Szczep, tło genetyczne
- Wiek, płeć, masa
- Stan zdrowia, źródło

### 3. **ResearchProtocol** - Protokoły badań
- Typy: in vitro, in vivo, ex vivo, computational
- Cel, metodologia, wersja
- Historia zmian

### 4. **Experiment** - Eksperymenty
- Status: planning, ongoing, completed, on_hold, cancelled
- Daty start/end
- Główny badacz, laboratorium
- Relacje N-M do linii komórkowych i modeli zwierzęcych

### 5. **ExperimentSample** - Próbki in vitro (N-M)
- Połączenie Experiment ↔ CellLine
- Traktowanie, stężenie, czas trwania
- Liczba replikat

### 6. **ExperimentAnimal** - Zwierzęta in vivo (N-M)
- Połączenie Experiment ↔ AnimalModel
- Grupa terapii, dawka
- Droga podania, liczba zwierząt

### 7. **Result** - Wyniki eksperymentów
- Nazwa parametru (np. cell viability, tumor size)
- Wartość i jednostka
- Metoda pomiaru (MTT assay, flow cytometry, itp.)

### 8. **GeneExpression** - Ekspresja genów
- Nazwa genu, ID (ENSG)
- Poziom ekspresji (fold change)
- Metody: qPCR, RNA-Seq, Microarray, In Situ, Immunohistochemistry, Western Blot
- Wartość p, przedział ufności
- Referencyjny gen (GAPDH)

### 9. **Documentation** - Dokumentacja
- Notatki, zmiany protokołu, raporty incydentów
- Załączniki plików
- Autor, daty

## API Endpoints

### Authentication
```
POST /api/auth/token/          # Uzyskaj token (username/password)
```

### Cell Lines
```
GET    /api/cell-lines/                    # Lista linii
POST   /api/cell-lines/                    # Nowa linia
GET    /api/cell-lines/{id}/               # Szczegóły
PUT    /api/cell-lines/{id}/               # Edycja
DELETE /api/cell-lines/{id}/               # Usuwanie

GET    /api/cell-lines/by_type/?type=cancer    # Filtruj po typie
GET    /api/cell-lines/{id}/experiments/       # Eksperymenty dla linii
```

### Animal Models
```
GET    /api/animal-models/                      # Lista modeli
POST   /api/animal-models/                      # Nowy model
GET    /api/animal-models/{id}/                 # Szczegóły
PUT    /api/animal-models/{id}/                 # Edycja
DELETE /api/animal-models/{id}/                 # Usuwanie

GET    /api/animal-models/by_species/?species=mouse  # Filtruj po gatunku
```

### Research Protocols
```
GET    /api/protocols/              # Lista protokołów
POST   /api/protocols/              # Nowy protokół
GET    /api/protocols/{id}/         # Szczegóły
PUT    /api/protocols/{id}/         # Edycja
DELETE /api/protocols/{id}/         # Usuwanie

GET    /api/protocols/{id}/experiments/  # Eksperymenty używające protokołu
```

### Experiments
```
GET    /api/experiments/                           # Lista
POST   /api/experiments/                           # Nowy eksperyment
GET    /api/experiments/{id}/                      # Szczegóły pełne
PUT    /api/experiments/{id}/                      # Edycja
DELETE /api/experiments/{id}/                      # Usuwanie

GET    /api/experiments/{id}/summary/                    # Podsumowanie
GET    /api/experiments/{id}/results_report/            # Raport wyników
GET    /api/experiments/{id}/gene_expression_report/    # Raport ekspresji genów
GET    /api/experiments/{id}/documentation/            # Dokumentacja
```

### Results
```
GET    /api/results/          # Lista wyników
POST   /api/results/          # Nowy wynik
GET    /api/results/{id}/     # Szczegóły
PUT    /api/results/{id}/     # Edycja
DELETE /api/results/{id}/     # Usuwanie
```

### Gene Expression
```
GET    /api/gene-expressions/          # Lista
POST   /api/gene-expressions/          # Nowy wpis
GET    /api/gene-expressions/{id}/     # Szczegóły
PUT    /api/gene-expressions/{id}/     # Edycja
DELETE /api/gene-expressions/{id}/     # Usuwanie
```

### Experiment Samples (in vitro)
```
GET    /api/samples/          # Lista próbek
POST   /api/samples/          # Nowa próbka
GET    /api/samples/{id}/     # Szczegóły
PUT    /api/samples/{id}/     # Edycja
DELETE /api/samples/{id}/     # Usuwanie
```

### Experiment Animals (in vivo)
```
GET    /api/animals/          # Lista zwierząt
POST   /api/animals/          # Nowe zwierzę
GET    /api/animals/{id}/     # Szczegóły
PUT    /api/animals/{id}/     # Edycja
DELETE /api/animals/{id}/     # Usuwanie
```

### Documentation
```
GET    /api/documentation/          # Lista docs
POST   /api/documentation/          # Nowy dokument
GET    /api/documentation/{id}/     # Szczegóły
PUT    /api/documentation/{id}/     # Edycja
DELETE /api/documentation/{id}/     # Usuwanie
```

## Filtry i wyszukiwanie

### Filtry
- Cell Lines: `cell_type`, `origin`, `tissue_type`
- Animal Models: `species`, `strain`, `sex`
- Experiments: `status`, `protocol`, `lab`
- Results: `experiment`, `parameter_name`, `method`
- Gene Expression: `gene_name`, `measurement_method`

### Wyszukiwanie
```
GET /api/cell-lines/?search=HeLa
GET /api/experiments/?search=tumor
GET /api/gene-expressions/?search=BRCA1
```

### Sortowanie
```
GET /api/experiments/?ordering=start_date
GET /api/experiments/?ordering=-created_date
```

## Instalacja i uruchomienie

### 1. Zainstaluj zależności
```bash
pip install -r requirements.txt
```

### 2. Migracje
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Stwórz superusera
```bash
python manage.py createsuperuser
```

### 4. Uruchom serwer
```bash
python manage.py runserver
```

API będzie dostępne pod adresem: `http://localhost:8000/api/`
Admin: `http://localhost:8000/admin/`

## Uwierzytelnianie

### Token-based authentication
```bash
# Uzyskaj token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'

# Użyj token w requestach
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/experiments/
```

## Przykładowe API requests

### Stwórz nową linię komórkową
```bash
curl -X POST http://localhost:8000/api/cell-lines/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "HeLa",
    "cell_type": "cancer",
    "origin": "human",
    "tissue_type": "epithelial",
    "passage_number": 150
  }'
```

### Stwórz eksperyment
```bash
curl -X POST http://localhost:8000/api/experiments/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Drug efficacy test",
    "protocol": 1,
    "status": "ongoing",
    "start_date": "2025-01-15",
    "principal_investigator": 1,
    "lab": "Lab A"
  }'
```

### Dodaj próbkę do eksperymentu
```bash
curl -X POST http://localhost:8000/api/samples/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "experiment": 1,
    "cell_line": 1,
    "treatment": "Drug X",
    "concentration": 10,
    "concentration_unit": "µM",
    "duration_hours": 24,
    "replicate_number": 3
  }'
```

### Dodaj wynik
```bash
curl -X POST http://localhost:8000/api/results/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "experiment": 1,
    "parameter_name": "cell_viability",
    "value": 75.5,
    "unit": "%",
    "method": "MTT assay",
    "sample": 1
  }'
```

### Pobierz raport eksperymentu
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/experiments/1/summary/
```

## GitHub Setup

### Inicjalizacja repozytorium
```bash
cd /workspaces/codespaces-django
git init
git add .
git commit -m "Initial commit: Medical research database with Django REST API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/medical-research-db.git
git push -u origin main
```

### .gitignore
```
__pycache__/
*.pyc
*.pyo
db.sqlite3
.env
.venv/
venv/
*.egg-info/
.DS_Store
hello_world/media/
hello_world/staticfiles/
```

## Struktura relacji N-M

```
Experiment (1) ---> (*) ExperimentSample <--- (*) CellLine
  |
  +---> (*) ExperimentAnimal <--- (*) AnimalModel

Result references: Experiment + ExperimentSample (lub ExperimentAnimal)

GeneExpression references: ExperimentSample (in vitro) lub ExperimentAnimal (in vivo)

Documentation references: Experiment
```

## Zaawansowane funkcjonalności

### 1. Raporty
- **Raport wyników**: Podsumowanie wszystkich pomiarów z kalkulacją średniej, min, max, sumy
- **Raport ekspresji genów**: Grupowanie po genach z metadanymi

### 2. Filtrowanie zaawansowane
- Kombinacja filtrów (status + lab + data)
- Wyszukiwanie pełnotekstowe

### 3. Autoryzacja
- Token-based
- Śledzenie autora każdego wpisu

## Rozwijanie projektu

### Dodaj nowy model
1. Zdefiniuj w `models.py`
2. Stwórz serializer w `serializers.py`
3. Stwórz ViewSet w `views.py`
4. Zarejestruj w `admin.py`
5. Dodaj route w `urls.py`
6. Utwórz migracje: `python manage.py makemigrations`

### Dostęp do Django Admin
`http://localhost:8000/admin/` - pełne zarządzanie modelami

## Licencja

MIT License - dostępne do celów edukacyjnych i badawczych
