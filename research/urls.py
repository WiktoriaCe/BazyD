from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CellLineViewSet, AnimalModelViewSet, ResearchProtocolViewSet,
    ExperimentViewSet, ExperimentSampleViewSet, ExperimentAnimalViewSet,
    ResultViewSet, GeneExpressionViewSet, DocumentationViewSet
)

router = DefaultRouter()
router.register(r'cell-lines', CellLineViewSet, basename='cellline')
router.register(r'animal-models', AnimalModelViewSet, basename='animalmodel')
router.register(r'protocols', ResearchProtocolViewSet, basename='protocol')
router.register(r'experiments', ExperimentViewSet, basename='experiment')
router.register(r'samples', ExperimentSampleViewSet, basename='experimentsample')
router.register(r'animals', ExperimentAnimalViewSet, basename='experimentanimal')
router.register(r'results', ResultViewSet, basename='result')
router.register(r'gene-expressions', GeneExpressionViewSet, basename='geneexpression')
router.register(r'documentation', DocumentationViewSet, basename='documentation')

urlpatterns = [
    path('api/', include(router.urls)),
]
