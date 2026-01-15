from django.shortcuts import render
from django.db.models import Q, Count, Avg, Sum
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    CellLine, AnimalModel, ResearchProtocol, Experiment,
    ExperimentSample, ExperimentAnimal, Result, GeneExpression, Documentation
)
from .serializers import (
    CellLineSerializer, AnimalModelSerializer, ResearchProtocolSerializer,
    ExperimentListSerializer, ExperimentDetailSerializer, ExperimentCreateUpdateSerializer,
    ExperimentSampleSerializer, ExperimentAnimalSerializer, ResultSerializer,
    GeneExpressionSerializer, DocumentationSerializer
)


class CellLineViewSet(viewsets.ModelViewSet):
    """
    API dla linii komórkowych.
    Obsługuje CRUD operacje.
    """
    queryset = CellLine.objects.all()
    serializer_class = CellLineSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cell_type', 'origin', 'tissue_type']
    search_fields = ['name', 'origin', 'tissue_type', 'description']
    ordering_fields = ['name', 'created_date', 'passage_number']
    ordering = ['name']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Pobierz linie komórkowe pogrupowane po typie"""
        cell_type = request.query_params.get('type')
        if cell_type:
            queryset = self.queryset.filter(cell_type=cell_type)
        else:
            queryset = self.queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def experiments(self, request, pk=None):
        """Pobierz wszystkie eksperymenty dla danej linii komórkowej"""
        cell_line = self.get_object()
        experiments = cell_line.experiments.all()
        serializer = ExperimentListSerializer(experiments, many=True)
        return Response(serializer.data)


class AnimalModelViewSet(viewsets.ModelViewSet):
    """
    API dla modeli zwierzęcych.
    Obsługuje CRUD operacje.
    """
    queryset = AnimalModel.objects.all()
    serializer_class = AnimalModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['species', 'strain', 'sex']
    search_fields = ['name', 'strain', 'species', 'health_status']
    ordering_fields = ['name', 'species', 'created_date', 'age_weeks']
    ordering = ['species', 'name']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_species(self, request):
        """Pobierz modele pogrupowane po gatunku"""
        species = request.query_params.get('species')
        if species:
            queryset = self.queryset.filter(species=species)
        else:
            queryset = self.queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ResearchProtocolViewSet(viewsets.ModelViewSet):
    """
    API dla protokołów badań.
    """
    queryset = ResearchProtocol.objects.all()
    serializer_class = ResearchProtocolSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['experiment_type']
    search_fields = ['title', 'description', 'objective']
    ordering_fields = ['created_date', 'title', 'version']
    ordering = ['-created_date']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def experiments(self, request, pk=None):
        """Pobierz eksperymenty korzystające z danego protokołu"""
        protocol = self.get_object()
        experiments = protocol.experiments.all()
        serializer = ExperimentListSerializer(experiments, many=True)
        return Response(serializer.data)


class ExperimentViewSet(viewsets.ModelViewSet):
    """
    API dla eksperymentów.
    Obsługuje pełne CRUD + dodatkowe akcje dla raportów.
    """
    queryset = Experiment.objects.prefetch_related('experiment_samples', 'experiment_animals', 'results')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'protocol', 'lab']
    search_fields = ['title', 'notes', 'lab', 'principal_investigator__username']
    ordering_fields = ['start_date', 'end_date', 'created_date', 'status']
    ordering = ['-start_date']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ExperimentDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ExperimentCreateUpdateSerializer
        else:
            return ExperimentListSerializer
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Pobierz podsumowanie eksperymentu"""
        experiment = self.get_object()
        
        summary_data = {
            'title': experiment.title,
            'status': experiment.status,
            'protocol': experiment.protocol.title,
            'start_date': experiment.start_date,
            'end_date': experiment.end_date,
            'samples_count': experiment.experiment_samples.count(),
            'animals_count': experiment.experiment_animals.aggregate(
                total=Sum('number_of_animals')
            )['total'] or 0,
            'results_count': experiment.results.count(),
            'gene_expressions_count': GeneExpression.objects.filter(
                Q(sample__experiment=experiment) | Q(animal_sample__experiment=experiment)
            ).count(),
        }
        return Response(summary_data)
    
    @action(detail=True, methods=['get'])
    def results_report(self, request, pk=None):
        """Wygeneruj raport wyników"""
        experiment = self.get_object()
        results = experiment.results.all()
        
        report_data = {
            'experiment': experiment.title,
            'results': ResultSerializer(results, many=True).data,
            'statistics': self._calculate_statistics(results)
        }
        return Response(report_data)
    
    @action(detail=True, methods=['get'])
    def gene_expression_report(self, request, pk=None):
        """Wygeneruj raport ekspresji genów"""
        experiment = self.get_object()
        gene_expressions = GeneExpression.objects.filter(
            Q(sample__experiment=experiment) | Q(animal_sample__experiment=experiment)
        ).distinct()
        
        # Grupuj po genach
        genes_data = {}
        for ge in gene_expressions:
            gene_name = ge.gene_name
            if gene_name not in genes_data:
                genes_data[gene_name] = []
            genes_data[gene_name].append({
                'expression_level': ge.expression_level,
                'method': ge.measurement_method,
                'p_value': ge.p_value,
                'confidence_interval': ge.confidence_interval
            })
        
        report_data = {
            'experiment': experiment.title,
            'genes': genes_data,
            'total_genes': len(genes_data),
            'measurements_count': gene_expressions.count()
        }
        return Response(report_data)
    
    @action(detail=True, methods=['get'])
    def documentation(self, request, pk=None):
        """Pobierz całą dokumentację eksperymentu"""
        experiment = self.get_object()
        docs = experiment.documentation.all()
        serializer = DocumentationSerializer(docs, many=True)
        return Response(serializer.data)
    
    def _calculate_statistics(self, results):
        """Kalkuluj statystyki z wyników"""
        if not results.exists():
            return {}
        
        values = [r.value for r in results]
        return {
            'count': len(values),
            'mean': sum(values) / len(values),
            'min': min(values),
            'max': max(values),
            'sum': sum(values)
        }


class ExperimentSampleViewSet(viewsets.ModelViewSet):
    """API dla próbek eksperymentów"""
    queryset = ExperimentSample.objects.all()
    serializer_class = ExperimentSampleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['experiment', 'cell_line', 'treatment']
    search_fields = ['treatment', 'notes']
    ordering_fields = ['replicate_number', 'concentration']


class ExperimentAnimalViewSet(viewsets.ModelViewSet):
    """API dla zwierząt w eksperymentach"""
    queryset = ExperimentAnimal.objects.all()
    serializer_class = ExperimentAnimalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['experiment', 'animal_model', 'treatment_group']
    search_fields = ['treatment_group', 'dosage']


class ResultViewSet(viewsets.ModelViewSet):
    """API dla wyników"""
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['experiment', 'parameter_name', 'method']
    search_fields = ['parameter_name', 'method', 'notes']
    ordering_fields = ['measurement_date', 'value']
    ordering = ['-measurement_date']


class GeneExpressionViewSet(viewsets.ModelViewSet):
    """API dla ekspresji genów"""
    queryset = GeneExpression.objects.all()
    serializer_class = GeneExpressionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gene_name', 'measurement_method']
    search_fields = ['gene_name', 'gene_id', 'reference_gene']
    ordering_fields = ['measurement_date', 'expression_level', 'p_value']
    ordering = ['-measurement_date']


class DocumentationViewSet(viewsets.ModelViewSet):
    """API dla dokumentacji"""
    queryset = Documentation.objects.all()
    serializer_class = DocumentationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['experiment', 'document_type']
    search_fields = ['title', 'content', 'document_type']
    ordering_fields = ['created_date', 'updated_date']
    ordering = ['-created_date']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

