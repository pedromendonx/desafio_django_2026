from django.contrib import admin
from .models import Curso

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('name', 'carga_horaria', 'valor_inscricao', 'status')
    search_fields = ('name',)
    list_filter = ('status',)
    ordering = ('name',)

