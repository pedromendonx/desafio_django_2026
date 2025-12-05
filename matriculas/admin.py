from django.contrib import admin
from .models import matriculas

@admin.register(matriculas)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'curso', 'data_matricula', 'status_pagamento')
    search_fields = ('aluno_nome', 'curso_nome')
    list_filter = ('status_pagamento', 'data_matricula')
    ordering = ('-data_matricula',)