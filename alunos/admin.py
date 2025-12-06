from django.contrib import admin
from .models import Aluno

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'CPF', 'data_ingresso')
    search_fields = ('name', 'email', 'CPF')
    list_filter = ('data_ingresso',)
    ordering = ('name',)

