# financeiro/views.py
from django.shortcuts import render
from matriculas.models import matriculas
from alunos.models import Aluno
from cursos.models import Curso
from django.db.models import Sum, Count

def dashboard(request):
    total_alunos = Aluno.objects.count()
    cursos_ativos = Curso.objects.filter(status=True).count()
    matriculas_pagas = matriculas.objects.filter(status='pago').count()
    matriculas_pendentes = matriculas.objects.filter(status='pendente').count()

    alunos_financeiro = []
    for aluno in Aluno.objects.all():
        total_pago = matriculas.objects.filter(aluno=aluno, status='pago').aggregate(Sum('curso__valor_inscricao'))['curso__valor_inscricao__sum'] or 0
        total_devido = matriculas.objects.filter(aluno=aluno, status='pendente').aggregate(Sum('curso__valor_inscricao'))['curso__valor_inscricao__sum'] or 0
        alunos_financeiro.append({
            'aluno': aluno.nome,
            'total_pago': total_pago,
            'total_devido': total_devido
        })

    context = {
        'total_alunos': total_alunos,
        'cursos_ativos': cursos_ativos,
        'matriculas_pagas': matriculas_pagas,
        'matriculas_pendentes': matriculas_pendentes,
        'alunos_financeiro': alunos_financeiro
    }
    return render(request, 'financeiro/dashboard.html', context)
