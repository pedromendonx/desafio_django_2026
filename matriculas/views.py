from rest_framework import viewsets
from .models import Matricula
from .serializers import MatriculaSerializer

class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
