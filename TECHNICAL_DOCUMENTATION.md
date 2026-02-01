# Dokumentacja techniczna - Medical Research Database


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

**Uwaga:** Interakcja z danymi odbywa się poprzez Django Admin oraz dedykowane widoki.

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

### Permissions & Access
- Application uses Django admin and standard Django auth for access control
- User tracking - Każdy wpis ma `created_by` lub `author`

### CORS
- Włączony dla `localhost:3000` i `localhost:8000`
- Konfiguracja w `settings.py`

### CSRF
- Standard Django CSRF token is used for web forms

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
2. Zarejestruj w `admin.py`
3. Stwórz migracje
4. Dodaj wszelkie potrzebne widoki lub strony w frontendzie

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

**Pytania?** Sprawdź [README.md](README.md) lub [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
