from django.shortcuts import render
from .models import Autor, Libro, Resena


def lista_libros(request):
    """Vista para mostrar la lista de todos los libros"""
    libros = Libro.objects.select_related('autor').prefetch_related('resenas').all()
    return render(request, 'biblioteca/lista_libros.html', {'libros': libros})


def detalle_libro(request, libro_id):
    """Vista para mostrar el detalle de un libro y sus reseñas"""
    libro = Libro.objects.select_related('autor').prefetch_related('resenas').get(pk=libro_id)
    return render(request, 'biblioteca/detalle_libro.html', {'libro': libro})


def lista_autores(request):
    """Vista para mostrar la lista de todos los autores"""
    autores = Autor.objects.prefetch_related('libros').all()
    return render(request, 'biblioteca/lista_autores.html', {'autores': autores})

