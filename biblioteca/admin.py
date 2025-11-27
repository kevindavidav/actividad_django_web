from django.contrib import admin
from .models import Autor, Libro, Resena


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nacionalidad', 'cantidad_libros')
    search_fields = ('nombre', 'nacionalidad')
    list_filter = ('nacionalidad',)
    
    def cantidad_libros(self, obj):
        """Muestra la cantidad de libros del autor"""
        return obj.libros.count()
    cantidad_libros.short_description = 'Cantidad de Libros'


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_publicacion', 'cantidad_resenas', 'calificacion_promedio')
    search_fields = ('titulo', 'autor__nombre', 'resumen')
    list_filter = ('autor', 'fecha_publicacion')
    date_hierarchy = 'fecha_publicacion'
    readonly_fields = ('calificacion_promedio',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'autor', 'fecha_publicacion')
        }),
        ('Contenido', {
            'fields': ('resumen',)
        }),
        ('Estadísticas', {
            'fields': ('calificacion_promedio',),
            'classes': ('collapse',)
        }),
    )
    
    def cantidad_resenas(self, obj):
        """Muestra la cantidad de reseñas del libro"""
        return obj.resenas.count()
    cantidad_resenas.short_description = 'Cantidad de Reseñas'
    
    def calificacion_promedio(self, obj):
        """Calcula y muestra la calificación promedio del libro"""
        resenas = obj.resenas.all()
        if resenas.exists():
            promedio = sum(r.calificacion for r in resenas) / resenas.count()
            return f"{promedio:.2f}/5"
        return "Sin reseñas"
    calificacion_promedio.short_description = 'Calificación Promedio'


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('libro', 'calificacion', 'fecha', 'texto_preview')
    search_fields = ('libro__titulo', 'texto')
    list_filter = ('calificacion', 'fecha')
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información de la Reseña', {
            'fields': ('libro', 'calificacion', 'fecha')
        }),
        ('Contenido', {
            'fields': ('texto',)
        }),
    )
    
    def texto_preview(self, obj):
        """Muestra un preview del texto de la reseña"""
        if len(obj.texto) > 100:
            return obj.texto[:100] + "..."
        return obj.texto
    texto_preview.short_description = 'Vista Previa'

