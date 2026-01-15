from rest_framework import serializers
from .models import (
    CellLine, AnimalModel, ResearchProtocol, Experiment,
    ExperimentSample, ExperimentAnimal, Result, GeneExpression, Documentation
)


class CellLineSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = CellLine
        fields = [
            'id', 'name', 'cell_type', 'origin', 'tissue_type',
            'description', 'passage_number', 'created_date', 'updated_date',
            'created_by', 'created_by_username'
        ]
        read_only_fields = ['created_date', 'updated_date', 'created_by']


class AnimalModelSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = AnimalModel
        fields = [
            'id', 'name', 'species', 'strain', 'genetic_background',
            'age_weeks', 'sex', 'weight_grams', 'health_status', 'source',
            'created_date', 'created_by', 'created_by_username'
        ]
        read_only_fields = ['created_date', 'created_by']


class ResearchProtocolSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = ResearchProtocol
        fields = [
            'id', 'title', 'description', 'experiment_type', 'objective',
            'methodology', 'version', 'created_date', 'updated_date',
            'created_by', 'created_by_username'
        ]
        read_only_fields = ['created_date', 'updated_date', 'created_by']


class ExperimentSampleSerializer(serializers.ModelSerializer):
    cell_line_name = serializers.CharField(source='cell_line.name', read_only=True)
    
    class Meta:
        model = ExperimentSample
        fields = [
            'id', 'experiment', 'cell_line', 'cell_line_name', 'treatment',
            'concentration', 'concentration_unit', 'duration_hours',
            'replicate_number', 'notes'
        ]


class ExperimentAnimalSerializer(serializers.ModelSerializer):
    animal_model_name = serializers.CharField(source='animal_model.name', read_only=True)
    
    class Meta:
        model = ExperimentAnimal
        fields = [
            'id', 'experiment', 'animal_model', 'animal_model_name',
            'treatment_group', 'dosage', 'route_of_administration',
            'number_of_animals', 'notes'
        ]


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = [
            'id', 'experiment', 'parameter_name', 'value', 'unit',
            'measurement_date', 'method', 'sample', 'animal_measurement', 'notes'
        ]
        read_only_fields = ['measurement_date']


class GeneExpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneExpression
        fields = [
            'id', 'gene_name', 'gene_id', 'sample', 'animal_sample',
            'expression_level', 'measurement_method', 'measurement_date',
            'reference_gene', 'confidence_interval', 'p_value', 'notes'
        ]
        read_only_fields = ['measurement_date']


class DocumentationSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Documentation
        fields = [
            'id', 'experiment', 'title', 'document_type', 'content',
            'author', 'author_username', 'created_date', 'updated_date',
            'file_attachment'
        ]
        read_only_fields = ['created_date', 'updated_date', 'author']


class ExperimentDetailSerializer(serializers.ModelSerializer):
    """Szczegółowy serializer eksperymentu z zagnieżdżonymi danymi"""
    principal_investigator_username = serializers.CharField(
        source='principal_investigator.username', read_only=True
    )
    protocol_title = serializers.CharField(source='protocol.title', read_only=True)
    experiment_samples = ExperimentSampleSerializer(many=True, read_only=True)
    experiment_animals = ExperimentAnimalSerializer(many=True, read_only=True)
    results = ResultSerializer(many=True, read_only=True)
    documentation = DocumentationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Experiment
        fields = [
            'id', 'title', 'protocol', 'protocol_title', 'status', 'start_date',
            'end_date', 'principal_investigator', 'principal_investigator_username',
            'lab', 'notes', 'created_date', 'updated_date',
            'experiment_samples', 'experiment_animals', 'results', 'documentation'
        ]
        read_only_fields = ['created_date', 'updated_date']


class ExperimentListSerializer(serializers.ModelSerializer):
    """Uproszczony serializer eksperymentu do list"""
    protocol_title = serializers.CharField(source='protocol.title', read_only=True)
    principal_investigator_username = serializers.CharField(
        source='principal_investigator.username', read_only=True
    )
    
    class Meta:
        model = Experiment
        fields = [
            'id', 'title', 'protocol', 'protocol_title', 'status', 'start_date',
            'end_date', 'principal_investigator', 'principal_investigator_username',
            'lab', 'created_date'
        ]


class ExperimentCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer do tworzenia i edytowania eksperymentów"""
    class Meta:
        model = Experiment
        fields = [
            'title', 'protocol', 'status', 'start_date', 'end_date',
            'principal_investigator', 'lab', 'notes'
        ]
