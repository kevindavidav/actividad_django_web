from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Autor, Libro, Resena
from .serializers import (
    AutorSerializer,
    LibroSerializer,
    LibroDetailSerializer,
    ResenaSerializer
)


class AutorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar autores.
    
    list: Retorna la lista de todos los autores
    retrieve: Retorna un autor específico
    create: Crea un nuevo autor
    update: Actualiza un autor completo
    partial_update: Actualiza parcialmente un autor
    destroy: Elimina un autor
    """
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre', 'nacionalidad']
    ordering_fields = ['nombre', 'nacionalidad']
    ordering = ['nombre']
    
    def get_queryset(self):
        """Sobrescribe get_queryset para agregar lógica condicional"""
        queryset = Autor.objects.prefetch_related('libros').all()
        
        # Filtrar por nacionalidad si se proporciona
        nacionalidad = self.request.query_params.get('nacionalidad', None)
        if nacionalidad:
            queryset = queryset.filter(nacionalidad__icontains=nacionalidad)
        
        return queryset
    
    def perform_create(self, serializer):
        """Sobrescribe perform_create para agregar lógica personalizada"""
        serializer.save()
    
    @action(detail=True, methods=['get'])
    def libros(self, request, pk=None):
        """Ruta personalizada: /api/authors/{id}/libros/"""
        autor = self.get_object()
        libros = autor.libros.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)


class LibroViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar libros.
    
    ═══════════════════════════════════════════════════════════════
    FILTROS Y ORDENAMIENTO CON DJANGO-FILTER - EXPLICACIÓN:
    ═══════════════════════════════════════════════════════════════
    
    1. DjangoFilterBackend: Permite filtrar usando django-filter
       - filterset_fields: Define campos que se pueden filtrar directamente
         Ejemplo: /api/books/?autor=2
       - También se pueden crear filtros personalizados en get_queryset()
    
    2. SearchFilter: Permite búsqueda en múltiples campos
       - search_fields: Define en qué campos buscar
       Ejemplo: /api/books/?search=García
    
    3. OrderingFilter: Permite ordenar los resultados
       - ordering_fields: Define campos por los que se puede ordenar
       - ordering: Ordenamiento por defecto
       Ejemplo: /api/books/?ordering=-publication_year (orden descendente por año)
                /api/books/?ordering=-fecha_publicacion (orden descendente por fecha)
                /api/books/?ordering=titulo (orden ascendente)
    ═══════════════════════════════════════════════════════════════
    
    ═══════════════════════════════════════════════════════════════
    PAGINACIÓN - EXPLICACIÓN:
    ═══════════════════════════════════════════════════════════════
    La paginación está configurada en settings.py en REST_FRAMEWORK:
    - PAGE_SIZE: 10 elementos por página
    - Se activa automáticamente cuando hay más de 10 resultados
    - Ejemplo: /api/books/?page=2
    
    La respuesta incluye:
    - count: Total de elementos
    - next: URL de la siguiente página
    - previous: URL de la página anterior
    - results: Lista de elementos de la página actual
    ═══════════════════════════════════════════════════════════════
    """
    queryset = Libro.objects.select_related('autor').prefetch_related('resenas').all()
    # DjangoFilterBackend: Filtros con django-filter (filterset_fields)
    # SearchFilter: Búsqueda en múltiples campos (search_fields)
    # OrderingFilter: Ordenamiento dinámico (ordering_fields)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['autor']  # Filtro directo: ?autor=2
    search_fields = ['titulo', 'resumen', 'autor__nombre']  # Búsqueda: ?search=García
    # Nota: 'publication_year' se anota en get_queryset() usando ExtractYear para poder ordenar por año
    # Para ordenar por año: ?ordering=-publication_year (descendente) o ?ordering=publication_year (ascendente)
    # También se puede usar: ?ordering=-fecha_publicacion (ordenar por fecha completa)
    ordering_fields = ['titulo', 'fecha_publicacion', 'publication_year']  # Ordenar: ?ordering=-publication_year
    ordering = ['-fecha_publicacion']  # Orden por defecto
    
    def get_serializer_class(self):
        """Retorna diferentes serializadores según la acción"""
        if self.action == 'retrieve':
            return LibroDetailSerializer
        return LibroSerializer
    
    def get_queryset(self):
        """
        Sobrescribe get_queryset para agregar filtros dinámicos
        
        Anota el campo 'publication_year' para que pueda ser usado en ordenamiento.
        Se usa un nombre diferente para evitar conflicto con la propiedad @property 'year' del modelo.
        """
        from django.db.models.functions import ExtractYear
        
        queryset = Libro.objects.select_related('autor').prefetch_related('resenas').all()
        
        # Anotar el año con un nombre diferente para evitar conflicto con la propiedad @property year del modelo
        queryset = queryset.annotate(publication_year=ExtractYear('fecha_publicacion'))
        
        # Filtro por autor usando query param
        autor_id = self.request.query_params.get('author', None)
        if autor_id:
            queryset = queryset.filter(autor_id=autor_id)
        
        # Filtro por año
        year = self.request.query_params.get('year', None)
        if year:
            queryset = queryset.filter(fecha_publicacion__year=year)
        
        return queryset
    
    def perform_create(self, serializer):
        """Sobrescribe perform_create para agregar validaciones"""
        serializer.save()
    
    @action(detail=True, methods=['get'])
    def rating_promedio(self, request, pk=None):
        """
        ═══════════════════════════════════════════════════════════════
        RUTA PERSONALIZADA CON @action - EXPLICACIÓN:
        ═══════════════════════════════════════════════════════════════
        
        El decorador @action permite crear rutas personalizadas que no
        son parte de las operaciones CRUD estándar (list, create, retrieve, etc.)
        
        Parámetros del decorador:
        - detail=True: La ruta es para un objeto específico
          URL: /api/books/{id}/rating_promedio/
        - detail=False: La ruta es para la colección completa
          URL: /api/books/por_autor/
        - methods=['get']: Métodos HTTP permitidos (get, post, put, etc.)
        
        Esta ruta calcula el rating promedio de un libro específico
        basado en todas sus reseñas que tengan el campo rating.
        
        Ejemplo de uso:
        GET /api/books/1/rating_promedio/
        
        Respuesta:
        {
            "libro_id": 1,
            "titulo": "Cien años de soledad",
            "rating_promedio": 4.55,
            "total_resenas": 2,
            "resenas_con_rating": 2
        }
        ═══════════════════════════════════════════════════════════════
        """
        libro = self.get_object()
        reviews = libro.resenas.exclude(rating__isnull=True)
        
        if reviews.exists():
            from django.db.models import Avg
            promedio = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
            promedio = round(promedio, 2) if promedio else None
        else:
            promedio = None
        
        return Response({
            'libro_id': libro.id,
            'titulo': libro.titulo,
            'rating_promedio': promedio,
            'total_resenas': libro.resenas.count(),
            'resenas_con_rating': reviews.count()
        })
    
    @action(detail=False, methods=['get'])
    def por_autor(self, request):
        """
        ═══════════════════════════════════════════════════════════════
        RUTA PERSONALIZADA CON @action (detail=False) - EXPLICACIÓN:
        ═══════════════════════════════════════════════════════════════
        
        Esta es otra ruta personalizada, pero con detail=False, lo que
        significa que no requiere un ID específico en la URL.
        
        URL: /api/books/por_autor/?autor_id=1
        
        Esta ruta permite obtener todos los libros de un autor específico
        pasando el ID del autor como parámetro de consulta.
        ═══════════════════════════════════════════════════════════════
        """
        autor_id = request.query_params.get('autor_id', None)
        if autor_id:
            libros = Libro.objects.filter(autor_id=autor_id)
            serializer = self.get_serializer(libros, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Debe proporcionar autor_id como parámetro'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ResenaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar reseñas.
    
    Incluye filtros por libro y calificación.
    """
    queryset = Resena.objects.select_related('libro', 'libro__autor').all()
    serializer_class = ResenaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['libro', 'calificacion']
    search_fields = ['texto', 'libro__titulo']
    ordering_fields = ['fecha', 'calificacion', 'rating']
    ordering = ['-fecha']
    
    def get_queryset(self):
        """Sobrescribe get_queryset para agregar filtros dinámicos"""
        queryset = Resena.objects.select_related('libro', 'libro__autor').all()
        
        # Filtro por rating mínimo
        rating_min = self.request.query_params.get('rating_min', None)
        if rating_min:
            try:
                queryset = queryset.filter(rating__gte=float(rating_min))
            except ValueError:
                pass
        
        # Filtro por rating máximo
        rating_max = self.request.query_params.get('rating_max', None)
        if rating_max:
            try:
                queryset = queryset.filter(rating__lte=float(rating_max))
            except ValueError:
                pass
        
        return queryset
    
    def perform_create(self, serializer):
        """Sobrescribe perform_create para agregar lógica personalizada"""
        # Si no se proporciona rating, usar calificacion como base
        if not serializer.validated_data.get('rating'):
            calificacion = serializer.validated_data.get('calificacion', 0)
            serializer.save(rating=float(calificacion))
        else:
            serializer.save()

