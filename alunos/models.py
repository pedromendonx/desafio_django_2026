from django.db import models

class Aluno (models.Model): 
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    CPF = models.CharField(max_length=11, unique=True)
    data_ingresso = models.DateField()


