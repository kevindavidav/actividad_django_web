from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


def validar_nombre_no_vacio(value):
    """Validador personalizado: el nombre no puede estar vacío o contener solo espacios"""
    if not value or not value.strip():
        raise ValidationError('El nombre no puede estar vacío o contener solo espacios.')


def validar_resumen_minimo(value):
    """Validador personalizado: el resumen debe tener al menos 50 caracteres"""
    if len(value.strip()) < 50:
        raise ValidationError('El resumen debe tener al menos 50 caracteres.')


def validar_calificacion(value):
    """Validador personalizado: la calificación debe estar entre 1 y 5"""
    if value < 1 or value > 5:
        raise ValidationError('La calificación debe estar entre 1 y 5.')


class Autor(models.Model):
    nombre = models.CharField(
        max_length=100,
        validators=[validar_nombre_no_vacio],
        help_text="Nombre completo del autor"
    )
    nacionalidad = models.CharField(max_length=50, help_text="Nacionalidad del autor")
    
    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.nacionalidad})"


class Libro(models.Model):
    titulo = models.CharField(max_length=200, help_text="Título del libro")
    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        related_name='libros',
        help_text="Autor del libro"
    )
    fecha_publicacion = models.DateField(help_text="Fecha de publicación del libro")
    resumen = models.TextField(
        validators=[validar_resumen_minimo],
        help_text="Resumen del libro (mínimo 50 caracteres)"
    )
    
    @property
    def year(self):
        """Retorna el año de publicación"""
        return self.fecha_publicacion.year
    
    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['titulo']
    
    def __str__(self):
        return f"{self.titulo} - {self.autor.nombre}"


class Resena(models.Model):
    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        related_name='resenas',
        help_text="Libro al que pertenece la reseña"
    )
    texto = models.TextField(help_text="Texto de la reseña")
    calificacion = models.IntegerField(
        validators=[validar_calificacion],
        help_text="Calificación del 1 al 5"
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Rating del 0.0 al 5.0",
        null=True,
        blank=True
    )
    fecha = models.DateTimeField(
        default=timezone.now,
        help_text="Fecha de la reseña"
    )
    
    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"Reseña de {self.libro.titulo} - {self.calificacion}/5"

