from rest_framework.views import APIView
from rest_framework.response import Response
from alunos.models import Aluno
from matriculas.models import Matricula
from django.db.models import Sum

class FinanceiroAPI(APIView):
    def get(self, request):
        dados = []
        for aluno in Aluno.objects.all():
            total_pago = Matricula.objects.filter(aluno=aluno, status='pago').aggregate(Sum('curso__valor_inscricao'))['curso__valor_inscricao__sum'] or 0
            total_devido = Matricula.objects.filter(aluno=aluno, status='pendente').aggregate(Sum('curso__valor_inscricao'))['curso__valor_inscricao__sum'] or 0
            dados.append({
                'aluno': aluno.nome,
                'total_pago': total_pago,
                'total_devido': total_devido
            })
        return Response(dados)
