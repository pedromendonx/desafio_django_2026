from rest_framework import viewsets
from .models import Matricula
from .serializers import MatriculaSerializer
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer

class RelatorioMatriculas(APIView):
    def get(self, request):
        dados = (Matricula.objects
            .values('curso__nome')
            .annotate(total=Count('id')))
        return Response(dados)