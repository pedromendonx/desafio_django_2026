from django.db import models

# Create your models here.

class matriculas(models.Model):

    aluno = models.ForeignKey('alunos.Aluno', on_delete=models.CASCADE)
    curso = models.ForeignKey('cursos.Curso', on_delete=models.CASCADE)
    data_matricula = models.DateField(auto_now_add=True)
    status_matricula = models.CharField(choices=[('pago', 'Pago'), ('pendente', 'Pendente')], max_length=10)
    