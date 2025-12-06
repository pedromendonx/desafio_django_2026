from django.contrib import admin
from .models import Matricula

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'curso', 'data_matricula', 'status_matricula')
    search_fields = ('aluno_nome', 'curso_nome')
    list_filter = ('status_matricula', 'data_matricula')
    ordering = ('-data_matricula',)