from django.urls import path
from . import views

app_name = 'biblioteca'

urlpatterns = [
    path('', views.lista_libros, name='lista_libros'),
    path('libros/', views.lista_libros, name='lista_libros'),
    path('libros/<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
    path('autores/', views.lista_autores, name='lista_autores'),
]

