from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import AutorViewSet, LibroViewSet, ResenaViewSet

# Crear el router y registrar los viewsets
router = DefaultRouter()
router.register(r'authors', AutorViewSet, basename='author')
router.register(r'books', LibroViewSet, basename='book')
router.register(r'reviews', ResenaViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]

