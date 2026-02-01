# Dokumentacja techniczna - Medical Research Database

> **NOTE:** The API layer has been removed from this codebase (branch `remove-api`). The sections below referencing API behavior are retained for historical context but are no longer accurate.

## Architektura systemu

### Warstwa modeli (ORM)
```
research/models.py zawiera 9 głównych modeli:

1. CellLine - Linie komórkowe (in vitro)
2. AnimalModel - Modele zwierzęce (in vivo)
3. ResearchProtocol - Protokoły badawcze
4. Experiment - Główna encja eksperymentu
5. ExperimentSample - N-M między Experiment i CellLine
6. ExperimentAnimal - N-M między Experiment i AnimalModel
7. Result - Wyniki pomiarów
8. GeneExpression - Dane ekspresji genów
9. Documentation - Notatki i dokumentacja
```

### Warstwa API (REST)
```
ViewSets w views.py zapewniają:
- CRU operacje na wszystkich modelach
- Filtering, searching, ordering
- Custom actions (summary, reports)
- Permission checking
```

### Relacje bazy danych

#### Relacja N-M: Experiment ←→ CellLine
```python
# Via ExperimentSample
experiment.cell_lines.all()  # Pobierz linie dla eksperymentu
cell_line.experiments.all()  # Pobierz eksperymenty dla linii
ExperimentSample.objects.filter(experiment=exp, cell_line=cl)
```

#### Relacja N-M: Experiment ←→ AnimalModel
```python
# Via ExperimentAnimal
experiment.animal_models.all()
animal_model.experiments.all()
ExperimentAnimal.objects.filter(experiment=exp, animal_model=am)
```

## Specyfikacja API

### Authentication
- **Typ**: Token-based (DRF)
- **Endpoint**: `POST /api/auth/token/`
- **Użycie**: `Authorization: Token <token>`

### ViewSet Features

#### Filtração
```python
filterset_fields = ['field1', 'field2']  # Exact match
search_fields = ['field1', 'field2']     # Full-text search
```

#### Sorting
```python
ordering_fields = ['field1', '-field2']
ordering = ['-created_date']  # Default sort
```

#### Pagination
```python
DEFAULT_PAGINATION_CLASS: PageNumberPagination
PAGE_SIZE: 20 (konfigurowalne w query: ?page_size=50)
```

### Custom Actions

#### Experiment Summary
```
GET /api/experiments/{id}/summary/
Response:
{
  "title": "...",
  "status": "completed",
  "samples_count": 4,
  "animals_count": 10,
  "results_count": 20,
  "gene_expressions_count": 50
}
```

#### Results Report
```
GET /api/experiments/{id}/results_report/
Response:
{
  "experiment": "...",
  "results": [...],
  "statistics": {
    "count": 20,
    "mean": 75.5,
    "min": 45.0,
    "max": 100.0,
    "sum": 1510.0
  }
}
```

#### Gene Expression Report
```
GET /api/experiments/{id}/gene_expression_report/
Response:
{
  "experiment": "...",
  "genes": {
    "BRCA1": [
      {"expression_level": 2.5, "method": "qpcr", "p_value": 0.01},
      ...
    ],
    ...
  },
  "total_genes": 5,
  "measurements_count": 25
}
```

## Walidacja modeli

### CellLine
- `name` - Unikalny, max 100 znaków
- `cell_type` - Wybór z: cancer, normal, primary, stem, other
- `passage_number` - Min 0

### AnimalModel
- `age_weeks` - Min 0
- `weight_grams` - Min 0
- `sex` - Wybór z: M, F, unknown

### Result
- `value` - Float dowolny
- `unit` - Max 50 znaków
- `p_value` - 0.0 - 1.0 (dla statystyk)

### GeneExpression
- `expression_level` - Float (fold change)
- `p_value` - 0.0 - 1.0
- `measurement_method` - Wybór z 7 opcji

## Przepływy danych

### Tworzenie eksperymentu z próbkami
```
1. POST /api/experiments/
   └─ Response: {id: 1, ...}

2. POST /api/samples/
   └─ {"experiment": 1, "cell_line": 1, "treatment": "Drug X", ...}
   └─ Response: {id: 1, ...}

3. POST /api/results/
   └─ {"experiment": 1, "sample": 1, "parameter_name": "viability", ...}

4. GET /api/experiments/1/summary/
   └─ Podsumowanie eksperymentu
```

### Dodawanie ekspresji genów
```
1. Próbka bereits exists: ExperimentSample.id = 1

2. POST /api/gene-expressions/
   └─ {"sample": 1, "gene_name": "BRCA1", "expression_level": 2.5, ...}

3. GET /api/experiments/1/gene_expression_report/
   └─ Raport z wszystkimi genami
```

## Performance considerations

### Queries optimization
```python
# ViewSet prefetch
queryset = Experiment.objects.prefetch_related(
    'experiment_samples',
    'experiment_animals', 
    'results'
)
```

### Indeksy bazy danych
- `CellLine.name` - Unique
- `ExperimentSample (experiment, cell_line, treatment, concentration)` - Unique
- `ExperimentAnimal (experiment, animal_model, treatment_group)` - Unique
- Foreign keys - Automatyczne indeksy Django

## Bezpieczeństwo

### Permissions
- `IsAuthenticated` - Wymagany dla wszystkich endpoints
- Tokeny w `rest_framework.authtoken`
- User tracking - Każdy wpis ma `created_by` lub `author`

### CORS
- Włączony dla `localhost:3000` i `localhost:8000`
- Konfiguracja w `settings.py`

### CSRF
- StandardDjangoCSRFToken
- Wyłączony dla API (token auth)

## Migracje

### Struktura migrations
```
research/migrations/
└── 0001_initial.py  # Początkowa migracja
```

### Dodawanie nowych modeli
```bash
python manage.py makemigrations
python manage.py migrate
```

## Admin interface

### Features
- Inline editing (ExperimentSample, ExperimentAnimal, Result, Documentation)
- List filters
- Search fields
- Readonly fields

### Customization
```python
@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['field1', 'field2']
    list_filter = ['field1']
    search_fields = ['field1']
    inlines = [RelatedInline]
```

## Testing

### Uruchomianie testów
```bash
python manage.py test research
```

### Struktura testów
```
research/tests.py
- Model tests
- Serializer tests
- ViewSet tests
- Integration tests
```

## Deployment

### Production checklist
```
- [ ] SECRET_KEY zmieniona
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS skonfigurowane
- [ ] Database migrated
- [ ] Static files collected
- [ ] Superuser created
- [ ] HTTPS enabled
- [ ] CORS configured
```

### Environment variables
```
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=domain.com,www.domain.com
DATABASE_URL=postgresql://user:pass@host:port/db
```

### Gunicorn deployment
```bash
gunicorn hello_world.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --worker-class sync
```

## Rozszerzanie projektu

### Dodawanie nowego modelu
1. Zdefiniuj w `models.py`
2. Stwórz serializer w `serializers.py`
3. Stwórz ViewSet w `views.py`
4. Zarejestruj w `admin.py`
5. Dodaj route w `urls.py`
6. Stwórz migracje

### Przykład:
```python
# models.py
class NewModel(models.Model):
    name = models.CharField(max_length=100)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

# serializers.py
class NewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewModel
        fields = '__all__'

# views.py
class NewModelViewSet(viewsets.ModelViewSet):
    queryset = NewModel.objects.all()
    serializer_class = NewModelSerializer

# urls.py
router.register(r'new-models', NewModelViewSet)
```

## Debugging

### Django Debug
```bash
python manage.py shell
>>> from research.models import *
>>> Experiment.objects.all()
```

### API Testing
```bash
# Get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/token/ \
  -d username=admin \
  -d password=admin123 | grep -o '"token":"[^"]*' | cut -d'"' -f4)

# Test endpoint
curl -H "Authorization: Token $TOKEN" \
  http://localhost:8000/api/experiments/
```

### Logs
```bash
# Django debug
python manage.py runserver --verbosity 2

# Production (Gunicorn)
tail -f /var/log/gunicorn.log
```

## Znane limitacje

1. SQLite - Nie rekomendowane dla produkcji (use PostgreSQL)
2. File uploads - Przechowywane lokalnie (use S3 dla production)
3. Max results - 20 per page (konfigurowalne)
4. No pagination dla nested resources (możliwe do dodania)

## Roadmap

- [ ] Batch import z CSV
- [ ] Advanced statistics/charts
- [ ] Export do PDF/Excel
- [ ] Real-time notifications
- [ ] Multi-user collaboration
- [ ] Version history dla eksperymentów
- [ ] Mobile app
- [ ] Machine learning predictions

---


