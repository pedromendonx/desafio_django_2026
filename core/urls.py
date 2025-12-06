from django.contrib import admin
from django.urls import path
from financeiro.views import relatorio_page, TotalPagoSQLView, RelatorioMatriculasPorCursoSQL

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', relatorio_page, name='home'),

    path('api/sql/total-pago/', TotalPagoSQLView.as_view(), name='api_total_pago'),
    path('api/sql/matriculas-por-curso/', RelatorioMatriculasPorCursoSQL.as_view(), name='api_matriculas_curso'),
]