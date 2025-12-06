from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
import json

class TotalPagoSQLView(APIView):
    """
    Endpoint usando SQL bruto com cursor()
    Requisitos: JOIN + Aggregation (SUM, COUNT, GROUP BY)
    """
    
    def get(self, request):
        try:
            with connection.cursor() as cursor:
    

                cursor.execute("""
                    SELECT 
                        a.id as aluno_id,
                        a.name as aluno_nome,  -- CORRIGIDO: de a.nome para a.name
                        a.email,
                        a.cpf,
                        COUNT(m.id) as total_matriculas,
                        SUM(CASE WHEN m.status_pagamento = 'P' THEN 1 ELSE 0 END) as matriculas_pagas,
                        SUM(CASE WHEN m.status_pagamento = 'E' THEN 1 ELSE 0 END) as matriculas_pendentes,
                        SUM(CASE WHEN m.status_pagamento = 'P' THEN c.valor_inscricao ELSE 0 END) as total_pago,
                        SUM(CASE WHEN m.status_pagamento = 'E' THEN c.valor_inscricao ELSE 0 END) as total_devido,
                        SUM(c.valor_inscricao) as valor_total
                    FROM alunos_aluno a
                    LEFT JOIN matriculas_matricula m ON a.id = m.aluno_id
                    LEFT JOIN cursos_curso c ON m.curso_id = c.id
                    GROUP BY a.id, a.name, a.email, a.cpf 
                    ORDER BY a.name 
                """)
                
                columns = [col[0] for col in cursor.description]
                
                results = []
                for row in cursor.fetchall():
                    row_dict = dict(zip(columns, row))
                    
                    for key in ['total_pago', 'total_devido', 'valor_total']:
                        if row_dict[key] is not None:
                            row_dict[key] = float(row_dict[key])
                    
                    results.append(row_dict)
                
                return Response({
                    'status': 'success',
                    'data': results,
                    'total_alunos': len(results),
                    'query_info': {
                        'joins': 2,
                        'aggregations': ['SUM', 'COUNT', 'GROUP BY'],
                        'tables': ['alunos_aluno', 'matriculas_matricula', 'cursos_curso']
                    }
                })
                
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RelatorioMatriculasPorCursoSQL(APIView):
    """Endpoint adicional: total de matrículas por curso"""
    
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        c.id as curso_id,
                        c.name as curso_nome,
                        c.carga_horaria,
                        c.valor_inscricao,
                        c.status,
                        COUNT(m.id) as total_matriculas,
                        SUM(CASE WHEN m.status_pagamento = 'P' THEN 1 ELSE 0 END) as pagas,
                        SUM(CASE WHEN m.status_pagamento = 'E' THEN 1 ELSE 0 END) as pendentes,
                        SUM(CASE WHEN m.status_pagamento = 'P' THEN c.valor_inscricao ELSE 0 END) as receita_confirmada,
                        SUM(CASE WHEN m.status_pagamento = 'E' THEN c.valor_inscricao ELSE 0 END) as receita_pendente
                    FROM cursos_curso c
                    LEFT JOIN matriculas_matricula m ON c.id = m.curso_id
                    GROUP BY c.id, c.name, c.carga_horaria, c.valor_inscricao, c.status
                    ORDER BY total_matriculas DESC
                """)
                
                columns = [col[0] for col in cursor.description]
                results = []
                
                for row in cursor.fetchall():
                    row_dict = dict(zip(columns, row))
                    
                    for key in ['valor_inscricao', 'receita_confirmada', 'receita_pendente']:
                        if row_dict[key] is not None:
                            row_dict[key] = float(row_dict[key])
                    
                    results.append(row_dict)
                
                return Response({
                    'status': 'success',
                    'data': results
                })
                
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def relatorio_page(request):
    """Renderiza a página HTML do relatório"""
    return render(request, 'dashboard.html')