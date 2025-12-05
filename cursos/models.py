from django.db import models

# Create your models here.

class Curso (models.Model): 
    name = models.CharField(max_length=100)
    carga_horaria = models.IntegerField()
    valor_inscricao = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.BooleanField(default=True)
    