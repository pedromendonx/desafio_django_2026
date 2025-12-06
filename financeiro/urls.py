from django.urls import path
from .views import TotalPagoSQLView, RelatorioMatriculasPorCursoSQL

urlpatterns = [
    path('api/sql/total-pago/', TotalPagoSQLView.as_view(), name='sql_total_pago'),
    path('api/sql/matriculas-por-curso/', RelatorioMatriculasPorCursoSQL.as_view(), name='sql_matriculas_curso'),
]

urlpatterns = [
    path('', include('financeiro.urls')), 
]