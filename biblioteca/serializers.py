from rest_framework import serializers
from django.db import models
from .models import Autor, Libro, Resena


class AutorSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Autor"""
    cantidad_libros = serializers.IntegerField(read_only=True, source='libros.count')
    
    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'nacionalidad', 'cantidad_libros']


class ResenaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Resena"""
    
    class Meta:
        model = Resena
        fields = ['id', 'libro', 'texto', 'calificacion', 'rating', 'fecha']
        read_only_fields = ['fecha']


class LibroSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Libro con campos computados
    
    ═══════════════════════════════════════════════════════════════
    SERIALIZERMETHODFIELD - EXPLICACIÓN:
    ═══════════════════════════════════════════════════════════════
    SerializerMethodField permite crear campos personalizados que no
    están directamente en el modelo. Estos campos se calculan usando
    métodos que siguen el patrón get_<nombre_campo>.
    
    En este caso:
    - recent_reviews: Usa SerializerMethodField para obtener las 5
      reseñas más recientes del libro mediante el método get_recent_reviews()
    - rating_promedio: Calcula el promedio de ratings usando el método
      get_rating_promedio() que agrega los ratings de todas las reseñas
    ═══════════════════════════════════════════════════════════════
    """
    author_name = serializers.ReadOnlyField(source='autor.nombre')
    year = serializers.ReadOnlyField(source='fecha_publicacion.year')
    # SerializerMethodField: Campo computado que se calcula dinámicamente
    recent_reviews = serializers.SerializerMethodField()
    # SerializerMethodField: Calcula el rating promedio de las reseñas
    rating_promedio = serializers.SerializerMethodField()
    
    class Meta:
        model = Libro
        fields = [
            'id', 'titulo', 'autor', 'author_name', 
            'fecha_publicacion', 'year', 'resumen',
            'recent_reviews', 'rating_promedio'
        ]
    
    def get_recent_reviews(self, obj):
        """
        Método para SerializerMethodField 'recent_reviews'
        
        Este método se ejecuta automáticamente cuando se serializa un Libro.
        Retorna las 5 reseñas más recientes del libro, serializadas con
        ResenaSerializer.
        
        Args:
            obj: Instancia del modelo Libro que se está serializando
        
        Returns:
            Lista de diccionarios con los datos de las reseñas
        """
        reviews = obj.resenas.all().order_by('-fecha')[:5]
        return ResenaSerializer(reviews, many=True).data
    
    def get_rating_promedio(self, obj):
        """
        Método para SerializerMethodField 'rating_promedio'
        
        Calcula el rating promedio del libro basado en el campo rating
        de todas sus reseñas. Usa agregación de Django (Avg) para calcular
        el promedio de manera eficiente.
        
        Args:
            obj: Instancia del modelo Libro que se está serializando
        
        Returns:
            Float con el promedio redondeado a 2 decimales, o None si no hay reseñas
        """
        reviews = obj.resenas.exclude(rating__isnull=True)
        if reviews.exists():
            promedio = reviews.aggregate(
                avg_rating=models.Avg('rating')
            )['avg_rating']
            return round(promedio, 2) if promedio else None
        return None


class LibroDetailSerializer(LibroSerializer):
    """Serializador detallado para Libro con autor anidado"""
    autor = AutorSerializer(read_only=True)
    
    class Meta(LibroSerializer.Meta):
        fields = LibroSerializer.Meta.fields + ['autor']

