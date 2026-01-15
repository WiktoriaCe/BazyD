from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class CellLine(models.Model):
    """Linia komórkowa"""
    CELL_TYPE_CHOICES = [
        ('cancer', 'Cancer'),
        ('normal', 'Normal'),
        ('primary', 'Primary'),
        ('stem', 'Stem Cell'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    cell_type = models.CharField(max_length=20, choices=CELL_TYPE_CHOICES)
    origin = models.CharField(max_length=200)  # np. human, mouse, rat
    tissue_type = models.CharField(max_length=100)  # np. epithelial, neuronal
    description = models.TextField(blank=True)
    passage_number = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='cell_lines')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Cell Line'
        verbose_name_plural = 'Cell Lines'
    
    def __str__(self):
        return self.name


class AnimalModel(models.Model):
    """Model zwierzęcy"""
    SPECIES_CHOICES = [
        ('mouse', 'Mouse'),
        ('rat', 'Rat'),
        ('zebrafish', 'Zebrafish'),
        ('drosophila', 'Drosophila'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES)
    strain = models.CharField(max_length=100)  # np. C57BL/6, Sprague Dawley
    genetic_background = models.TextField(blank=True)
    age_weeks = models.IntegerField(validators=[MinValueValidator(0)])
    sex = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('unknown', 'Unknown')])
    weight_grams = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    health_status = models.CharField(max_length=200)
    source = models.CharField(max_length=200)  # dostawca/laboratorium
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='animal_models')
    
    class Meta:
        ordering = ['species', 'name']
    
    def __str__(self):
        return f"{self.get_species_display()} - {self.strain} ({self.name})"


class ResearchProtocol(models.Model):
    """Protokół badań"""
    EXPERIMENT_TYPE_CHOICES = [
        ('in_vitro', 'In Vitro'),
        ('in_vivo', 'In Vivo'),
        ('ex_vivo', 'Ex Vivo'),
        ('computational', 'Computational'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    experiment_type = models.CharField(max_length=20, choices=EXPERIMENT_TYPE_CHOICES)
    objective = models.TextField()
    methodology = models.TextField()
    version = models.IntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='protocols')
    
    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return f"{self.title} (v{self.version})"


class Experiment(models.Model):
    """Eksperyment"""
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=255)
    protocol = models.ForeignKey(ResearchProtocol, on_delete=models.PROTECT, related_name='experiments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    principal_investigator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='experiments_pi')
    lab = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Relacje N-M
    cell_lines = models.ManyToManyField(CellLine, through='ExperimentSample', related_name='experiments')
    animal_models = models.ManyToManyField(AnimalModel, through='ExperimentAnimal', related_name='experiments')
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title


class ExperimentSample(models.Model):
    """Połączenie między eksperymentem a linią komórkową (N-M)"""
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='experiment_samples')
    cell_line = models.ForeignKey(CellLine, on_delete=models.CASCADE)
    treatment = models.CharField(max_length=255, blank=True)  # np. exposure, drug
    concentration = models.FloatField(null=True, blank=True)
    concentration_unit = models.CharField(max_length=50, blank=True)  # µM, ng/ml, etc.
    duration_hours = models.FloatField(null=True, blank=True)
    replicate_number = models.IntegerField(default=1)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('experiment', 'cell_line', 'treatment', 'concentration')
    
    def __str__(self):
        return f"{self.experiment.title} - {self.cell_line.name}"


class ExperimentAnimal(models.Model):
    """Połączenie między eksperymentem a modelem zwierzęcym (N-M)"""
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='experiment_animals')
    animal_model = models.ForeignKey(AnimalModel, on_delete=models.CASCADE)
    treatment_group = models.CharField(max_length=100)  # np. control, treatment_1
    dosage = models.CharField(max_length=100, blank=True)  # np. 10 mg/kg
    route_of_administration = models.CharField(max_length=100, blank=True)  # oral, IV, IP
    number_of_animals = models.IntegerField(validators=[MinValueValidator(1)])
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('experiment', 'animal_model', 'treatment_group')
    
    def __str__(self):
        return f"{self.experiment.title} - {self.treatment_group}"


class Result(models.Model):
    """Wyniki eksperymentu"""
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='results')
    parameter_name = models.CharField(max_length=255)  # np. cell viability, tumor size
    value = models.FloatField()
    unit = models.CharField(max_length=50)  # %, mm, µg/ml
    measurement_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=200)  # np. MTT assay, flow cytometry
    sample = models.ForeignKey(ExperimentSample, null=True, blank=True, on_delete=models.SET_NULL)
    animal_measurement = models.ForeignKey(ExperimentAnimal, null=True, blank=True, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-measurement_date']
    
    def __str__(self):
        return f"{self.parameter_name}: {self.value} {self.unit}"


class GeneExpression(models.Model):
    """Ekspresja genów"""
    EXPRESSION_METHOD_CHOICES = [
        ('qpcr', 'qPCR'),
        ('rna_seq', 'RNA-Seq'),
        ('microarray', 'Microarray'),
        ('in_situ', 'In Situ Hybridization'),
        ('immunohistochemistry', 'Immunohistochemistry'),
        ('western_blot', 'Western Blot'),
        ('other', 'Other'),
    ]
    
    gene_name = models.CharField(max_length=100)
    gene_id = models.CharField(max_length=50, blank=True)  # np. ENSG00000000003
    sample = models.ForeignKey(ExperimentSample, null=True, blank=True, on_delete=models.CASCADE, related_name='gene_expressions')
    animal_sample = models.ForeignKey(ExperimentAnimal, null=True, blank=True, on_delete=models.CASCADE)
    expression_level = models.FloatField()  # fold change, normalized counts
    measurement_method = models.CharField(max_length=30, choices=EXPRESSION_METHOD_CHOICES)
    measurement_date = models.DateTimeField(auto_now_add=True)
    reference_gene = models.CharField(max_length=100, blank=True)  # np. GAPDH
    confidence_interval = models.CharField(max_length=100, blank=True)  # np. 1.2-1.8
    p_value = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-measurement_date']
    
    def __str__(self):
        return f"{self.gene_name} - {self.expression_level} ({self.measurement_method})"


class Documentation(models.Model):
    """Dokumentacja i notatki"""
    DOC_TYPE_CHOICES = [
        ('note', 'Note'),
        ('protocol_amendment', 'Protocol Amendment'),
        ('incident_report', 'Incident Report'),
        ('data_quality_report', 'Data Quality Report'),
        ('other', 'Other'),
    ]
    
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='documentation')
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=30, choices=DOC_TYPE_CHOICES)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    file_attachment = models.FileField(upload_to='experiment_docs/%Y/%m/%d/', null=True, blank=True)
    
    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return self.title
