from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from .models import (
    CellLine, AnimalModel, ResearchProtocol, Experiment,
    ExperimentSample, ExperimentAnimal, Result, GeneExpression, Documentation
)





@admin.register(ResearchProtocol)
class ResearchProtocolAdmin(admin.ModelAdmin):
    list_display = ('index_number', 'title', 'experiment_type', 'version', 'created_by', 'created_date')
    list_filter = ('experiment_type', 'created_date')
    search_fields = ('title', 'description', 'objective')
    readonly_fields = ('created_date', 'updated_date')


class ExperimentSampleInline(admin.TabularInline):
    model = ExperimentSample
    extra = 1


class ExperimentSampleInlineForCellLine(admin.TabularInline):
    model = ExperimentSample
    fk_name = 'cell_line'
    fields = ('index_number', 'experiment', 'treatment', 'concentration', 'replicate_number')
    readonly_fields = ('index_number',)
    extra = 0


class ExperimentAnimalInline(admin.TabularInline):
    model = ExperimentAnimal
    extra = 1


class ExperimentAnimalInlineForAnimalModel(admin.TabularInline):
    model = ExperimentAnimal
    fk_name = 'animal_model'
    fields = ('index_number', 'experiment', 'treatment_group', 'number_of_animals')
    readonly_fields = ('index_number',)
    extra = 0


class ResultInline(admin.TabularInline):
    model = Result
    extra = 1


class DocumentationInline(admin.TabularInline):
    model = Documentation
    extra = 1


@admin.register(CellLine)
class CellLineAdmin(admin.ModelAdmin):
    list_display = ('index_number', 'name', 'cell_type', 'origin', 'tissue_type', 'passage_number', 'created_by', 'users_using', 'experiments_indexes', 'sample_indexes')
    list_filter = ('cell_type', 'origin', 'tissue_type', 'created_date')
    search_fields = ('name', 'origin', 'tissue_type')
    readonly_fields = ('created_date', 'updated_date')
    inlines = (ExperimentSampleInlineForCellLine,)

    def experiments_indexes(self, obj):
        qs = obj.experiments.order_by('index_number').values_list('index_number', flat=True)
        return ", ".join(str(x) for x in qs if x is not None)
    experiments_indexes.short_description = 'Experiments (index)'

    def sample_indexes(self, obj):
        # some models use explicit related_name, others use default <model>_set
        if hasattr(obj, 'experiment_samples'):
            qs = obj.experiment_samples
        else:
            qs = obj.experimentsample_set
        qs = qs.order_by('index_number').values_list('index_number', flat=True)
        return ", ".join(str(x) for x in qs if x is not None)
    sample_indexes.short_description = 'Samples (index)'

    def users_using(self, obj):
        # users who created the cell line
        users = []
        if getattr(obj, 'created_by', None):
            users.append(obj.created_by)

        # users who are principal investigators of experiments using this cell line
        manager = getattr(obj, 'experiment_samples', None)
        if manager is None:
            manager = obj.experimentsample_set

        for s in manager.select_related('experiment__principal_investigator').all():
            pi = getattr(s, 'experiment', None)
            if pi:
                user = getattr(pi, 'principal_investigator', None)
                if user and user not in users:
                    users.append(user)

        if not users:
            return '-'

        return format_html_join(', ', '<a href="{}">{}</a>', (
            (reverse('admin:auth_user_change', args=(u.pk,)), (u.get_full_name() or u.username)) for u in users
        ))
    users_using.short_description = 'Użytkownicy używający'


@admin.register(AnimalModel)
class AnimalModelAdmin(admin.ModelAdmin):
    list_display = ('index_number', 'name', 'species', 'strain', 'sex', 'age_weeks', 'created_by', 'users_using', 'experiments_indexes', 'animal_group_indexes')
    list_filter = ('species', 'strain', 'sex', 'created_date')
    search_fields = ('name', 'strain', 'species')
    readonly_fields = ('created_date',)
    inlines = (ExperimentAnimalInlineForAnimalModel,)

    def experiments_indexes(self, obj):
        qs = obj.experiments.order_by('index_number').values_list('index_number', flat=True)
        return ", ".join(str(x) for x in qs if x is not None)
    experiments_indexes.short_description = 'Experiments (index)'

    def animal_group_indexes(self, obj):
        if hasattr(obj, 'experiment_animals'):
            qs = obj.experiment_animals
        else:
            qs = obj.experimentanimal_set
        qs = qs.order_by('index_number').values_list('index_number', flat=True)
        return ", ".join(str(x) for x in qs if x is not None)
    animal_group_indexes.short_description = 'Animal groups (index)'

    def users_using(self, obj):
        users = []
        if getattr(obj, 'created_by', None):
            users.append(obj.created_by)

        manager = getattr(obj, 'experiment_animals', None)
        if manager is None:
            manager = obj.experimentanimal_set

        for a in manager.select_related('experiment__principal_investigator').all():
            exp = getattr(a, 'experiment', None)
            if exp:
                user = getattr(exp, 'principal_investigator', None)
                if user and user not in users:
                    users.append(user)

        if not users:
            return '-'

        return format_html_join(', ', '<a href="{}">{}</a>', (
            (reverse('admin:auth_user_change', args=(u.pk,)), (u.get_full_name() or u.username)) for u in users
        ))
    users_using.short_description = 'Użytkownicy używający'


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('index_number', 'title', 'status', 'protocol', 'start_date', 'end_date', 'principal_investigator', 'lab')
    list_filter = ('status', 'start_date', 'protocol', 'lab')
    search_fields = ('title', 'notes', 'lab')
    readonly_fields = ('created_date', 'updated_date')
    
    inlines = [ExperimentSampleInline, ExperimentAnimalInline, ResultInline, DocumentationInline]


@admin.register(ExperimentSample)
class ExperimentSampleAdmin(admin.ModelAdmin):
    list_display = ('index_number', 'experiment', 'cell_line', 'treatment', 'concentration', 'replicate_number')
    list_filter = ('experiment', 'cell_line', 'treatment')
    search_fields = ('treatment', 'notes')


@admin.register(ExperimentAnimal)
class ExperimentAnimalAdmin(admin.ModelAdmin):
    list_display = ('index_number', 'experiment', 'animal_model', 'treatment_group', 'number_of_animals')
    list_filter = ('experiment', 'animal_model', 'treatment_group')
    search_fields = ('treatment_group', 'dosage')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('index_number', 'experiment', 'parameter_name', 'value', 'unit', 'measurement_date', 'method')
    list_filter = ('experiment', 'parameter_name', 'method', 'measurement_date')
    search_fields = ('parameter_name', 'method', 'notes')
    readonly_fields = ('measurement_date',)


@admin.register(GeneExpression)
class GeneExpressionAdmin(admin.ModelAdmin):
    list_display = ('index_number', 'gene_name', 'gene_id', 'expression_level', 'measurement_method', 'measurement_date', 'p_value')
    list_filter = ('gene_name', 'measurement_method', 'measurement_date')
    search_fields = ('gene_name', 'gene_id', 'reference_gene')
    readonly_fields = ('measurement_date',)


@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    list_display = ('index_number', 'title', 'experiment', 'document_type', 'author', 'created_date')
    list_filter = ('document_type', 'experiment', 'created_date')
    search_fields = ('title', 'content', 'document_type')
    readonly_fields = ('created_date', 'updated_date')


# Register custom User admin to show user id and related indexes
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib import admin as django_admin

try:
    django_admin.site.unregister(User)
except Exception:
    pass


@django_admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'experiments_indexes', 'cell_lines_indexes', 'animal_models_indexes')

    def experiments_indexes(self, obj):
        qs = getattr(obj, 'experiments_pi', None)
        if qs is None:
            qs = obj.experiment_set
        qs = qs.order_by('index_number').values_list('index_number', flat=True)
        return ", ".join(str(x) for x in qs if x is not None)
    experiments_indexes.short_description = 'Experiments (index)'

    def cell_lines_indexes(self, obj):
        qs = getattr(obj, 'cell_lines', None)
        if qs is None:
            qs = obj.cellline_set
        qs = qs.order_by('index_number').values_list('index_number', flat=True)
        return ", ".join(str(x) for x in qs if x is not None)
    cell_lines_indexes.short_description = 'CellLines (index)'

    def animal_models_indexes(self, obj):
        qs = getattr(obj, 'animal_models', None)
        if qs is None:
            qs = obj.animalmodel_set
        qs = qs.order_by('index_number').values_list('index_number', flat=True)
        return ", ".join(str(x) for x in qs if x is not None)
    animal_models_indexes.short_description = 'AnimalModels (index)'

