from rest_framework import routers
from django.urls import path, include
from matriculas import MatriculaViewSet

router = routers.DefaultRouter()
router.register(r'matriculas', MatriculaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
