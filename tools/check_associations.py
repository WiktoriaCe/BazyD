from django.contrib.auth.models import User

for u in User.objects.all():
    # skip superusers without related objects if desired
    cl_count = u.cell_lines.count() if hasattr(u, 'cell_lines') else 0
    am_count = u.animal_models.count() if hasattr(u, 'animal_models') else 0
    exp_count = u.experiments_pi.count() if hasattr(u, 'experiments_pi') else 0
    print(f"{u.username}: cell_lines={cl_count}, animal_models={am_count}, experiments={exp_count}")
