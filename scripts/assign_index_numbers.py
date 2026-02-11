"""
Skrypt przypisujący brakujące wartości `index_number` dla modeli w aplikacji `research`.

Uruchom z poziomu kontenera dev lub środowiska, gdzie działa Django:

    python scripts/assign_index_numbers.py

Skrypt ustawia `index_number` zaczynając od (max istniejący + 1) dla każdego modelu.
"""
import os
import django
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world.settings')
django.setup()

from research import models

MODEL_NAMES = [
    'CellLine', 'AnimalModel', 'ResearchProtocol', 'Experiment',
    'ExperimentSample', 'ExperimentAnimal', 'Result', 'GeneExpression', 'Documentation'
]


def assign_for_model(model_cls):
    qs = model_cls.objects.all()
    # znajdź maksymalny index_number
    max_idx = qs.exclude(index_number__isnull=True).aggregate(models.models.Max('index_number'))['index_number__max']
    if max_idx is None:
        start = 1
    else:
        start = int(max_idx) + 1

    to_update = qs.filter(index_number__isnull=True).order_by('pk')
    count = to_update.count()
    if count == 0:
        print(f"{model_cls.__name__}: brak brakujących index_number")
        return 0

    print(f"{model_cls.__name__}: przypisuję {count} index_number od {start}")
    i = start
    with transaction.atomic():
        for obj in to_update:
            obj.index_number = i
            obj.save(update_fields=['index_number'])
            i += 1

    print(f"{model_cls.__name__}: przypisano {count} index_number")
    return count


def main():
    total = 0
    for name in MODEL_NAMES:
        model_cls = getattr(models, name, None)
        if model_cls is None:
            print(f"Model {name} nie znaleziony w research.models, pomijam.")
            continue
        try:
            total += assign_for_model(model_cls)
        except Exception as e:
            print(f"Błąd przy przydzielaniu index_number dla {name}: {e}")

    print(f"Gotowe. Przypisano łącznie {total} index_number.")


if __name__ == '__main__':
    main()
