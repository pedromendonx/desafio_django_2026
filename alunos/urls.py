from rest_framework import routers
from alunos import AlunoViewSet  
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'alunos', AlunoViewSet)  

urlpatterns = [
    path('', include(router.urls)),  
]