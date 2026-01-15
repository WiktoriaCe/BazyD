from django.contrib import admin
from .models import (
    CellLine, AnimalModel, ResearchProtocol, Experiment,
    ExperimentSample, ExperimentAnimal, Result, GeneExpression, Documentation
)


@admin.register(CellLine)
class CellLineAdmin(admin.ModelAdmin):
    list_display = ('name', 'cell_type', 'origin', 'tissue_type', 'passage_number', 'created_by')
    list_filter = ('cell_type', 'origin', 'tissue_type', 'created_date')
    search_fields = ('name', 'origin', 'tissue_type')
    readonly_fields = ('created_date', 'updated_date')


@admin.register(AnimalModel)
class AnimalModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'strain', 'sex', 'age_weeks', 'created_by')
    list_filter = ('species', 'strain', 'sex', 'created_date')
    search_fields = ('name', 'strain', 'species')
    readonly_fields = ('created_date',)


@admin.register(ResearchProtocol)
class ResearchProtocolAdmin(admin.ModelAdmin):
    list_display = ('title', 'experiment_type', 'version', 'created_by', 'created_date')
    list_filter = ('experiment_type', 'created_date')
    search_fields = ('title', 'description', 'objective')
    readonly_fields = ('created_date', 'updated_date')


class ExperimentSampleInline(admin.TabularInline):
    model = ExperimentSample
    extra = 1


class ExperimentAnimalInline(admin.TabularInline):
    model = ExperimentAnimal
    extra = 1


class ResultInline(admin.TabularInline):
    model = Result
    extra = 1


class DocumentationInline(admin.TabularInline):
    model = Documentation
    extra = 1


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'protocol', 'start_date', 'end_date', 'principal_investigator', 'lab')
    list_filter = ('status', 'start_date', 'protocol', 'lab')
    search_fields = ('title', 'notes', 'lab')
    readonly_fields = ('created_date', 'updated_date')
    
    inlines = [ExperimentSampleInline, ExperimentAnimalInline, ResultInline, DocumentationInline]


@admin.register(ExperimentSample)
class ExperimentSampleAdmin(admin.ModelAdmin):
    list_display = ('experiment', 'cell_line', 'treatment', 'concentration', 'replicate_number')
    list_filter = ('experiment', 'cell_line', 'treatment')
    search_fields = ('treatment', 'notes')


@admin.register(ExperimentAnimal)
class ExperimentAnimalAdmin(admin.ModelAdmin):
    list_display = ('experiment', 'animal_model', 'treatment_group', 'number_of_animals')
    list_filter = ('experiment', 'animal_model', 'treatment_group')
    search_fields = ('treatment_group', 'dosage')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('experiment', 'parameter_name', 'value', 'unit', 'measurement_date', 'method')
    list_filter = ('experiment', 'parameter_name', 'method', 'measurement_date')
    search_fields = ('parameter_name', 'method', 'notes')
    readonly_fields = ('measurement_date',)


@admin.register(GeneExpression)
class GeneExpressionAdmin(admin.ModelAdmin):
    list_display = ('gene_name', 'gene_id', 'expression_level', 'measurement_method', 'measurement_date', 'p_value')
    list_filter = ('gene_name', 'measurement_method', 'measurement_date')
    search_fields = ('gene_name', 'gene_id', 'reference_gene')
    readonly_fields = ('measurement_date',)


@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    list_display = ('title', 'experiment', 'document_type', 'author', 'created_date')
    list_filter = ('document_type', 'experiment', 'created_date')
    search_fields = ('title', 'content', 'document_type')
    readonly_fields = ('created_date', 'updated_date')

