from rest_framework import routers
from django.urls import path, include
from cursos import CursoViewSet

router = routers.DefaultRouter()
router.register(r'cursos', CursoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
