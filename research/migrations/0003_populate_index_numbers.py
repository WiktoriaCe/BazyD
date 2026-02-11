from django.db import migrations


def populate_index_numbers(apps, schema_editor):
    model_names = [
        'CellLine', 'AnimalModel', 'ResearchProtocol', 'Experiment',
        'ExperimentSample', 'ExperimentAnimal', 'Result', 'GeneExpression', 'Documentation'
    ]
    for name in model_names:
        Model = apps.get_model('research', name)
        # use .iterator() for memory efficiency
        for obj in Model.objects.all().iterator():
            if getattr(obj, 'index_number', None) in (None, ''):
                # prefer existing PK if available
                pk = getattr(obj, 'id', None)
                obj.index_number = pk if pk is not None else getattr(obj, 'pk', None)
                obj.save(update_fields=['index_number'])


def reverse_func(apps, schema_editor):
    # noop: do not reset index numbers on reverse
    return


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0002_animalmodel_index_number_cellline_index_number_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_index_numbers, reverse_func),
    ]
