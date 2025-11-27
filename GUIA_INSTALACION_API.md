# 🚀 Guía de Instalación - API REST con Django REST Framework

## Pasos para activar la API REST

### 1. Instalar las dependencias

```cmd
pip install -r requirements.txt
```

Esto instalará:
- Django REST Framework
- django-filter

### 2. Crear y aplicar migraciones

El modelo `Resena` ahora incluye un nuevo campo `rating` (FloatField):

```cmd
python manage.py makemigrations
python manage.py migrate
```

### 3. (Opcional) Actualizar datos existentes

Si ya tienes datos en la base de datos, puedes actualizar las reseñas existentes para incluir el campo `rating`:

```cmd
python manage.py shell
```

```python
from biblioteca.models import Resena

# Actualizar reseñas existentes para que rating = calificacion
for resena in Resena.objects.filter(rating__isnull=True):
    resena.rating = float(resena.calificacion)
    resena.save()
```

O simplemente ejecuta el script de poblar datos nuevamente (eliminará y recreará los datos):

```cmd
python biblioteca\poblar_datos.py
```

### 4. Ejecutar el servidor

```cmd
python manage.py runserver
```

### 5. Acceder a la API

- **Interfaz Browsable API**: http://127.0.0.1:8000/api/
- **Autores**: http://127.0.0.1:8000/api/authors/
- **Libros**: http://127.0.0.1:8000/api/books/
- **Reseñas**: http://127.0.0.1:8000/api/reviews/

## 🧪 Probar la API

### Desde el navegador

1. Abre http://127.0.0.1:8000/api/books/
2. Verás la interfaz Browsable API de DRF
3. Puedes probar los filtros directamente desde la interfaz

### Ejemplos de URLs para probar

```
# Filtrar libros por autor
http://127.0.0.1:8000/api/books/?author=2

# Ordenar libros por año (más recientes primero)
http://127.0.0.1:8000/api/books/?ordering=-year

# Paginación
http://127.0.0.1:8000/api/books/?page=2

# Filtrar reseñas por rating
http://127.0.0.1:8000/api/reviews/?rating_min=4.0&rating_max=5.0

# Obtener rating promedio de un libro
http://127.0.0.1:8000/api/books/1/rating_promedio/
```

### Desde Postman o Insomnia

1. Importa los endpoints desde la documentación
2. Prueba las peticiones GET, POST, PUT, PATCH, DELETE
3. Verifica las respuestas JSON

### Desde curl (línea de comandos)

```bash
# Obtener todos los libros
curl http://127.0.0.1:8000/api/books/

# Crear un nuevo autor
curl -X POST http://127.0.0.1:8000/api/authors/ \
  -H "Content-Type: application/json" \
  -d "{\"nombre\": \"Nuevo Autor\", \"nacionalidad\": \"Española\"}"

# Obtener rating promedio de un libro
curl http://127.0.0.1:8000/api/books/1/rating_promedio/
```

## 📋 Estructura de Archivos Creados

```
biblioteca/
├── serializers.py      # Serializadores con campos computados
├── viewsets.py         # ViewSets personalizados con rutas @action
├── api_urls.py         # Configuración de routers
└── models.py           # Modelo actualizado con campo rating
```

## ✅ Verificación

Para verificar que todo funciona:

1. Accede a http://127.0.0.1:8000/api/books/
2. Deberías ver la lista de libros con paginación
3. Prueba los filtros desde la interfaz
4. Verifica que las rutas personalizadas funcionen:
   - `/api/books/1/rating_promedio/`
   - `/api/authors/1/libros/`

## 📚 Documentación Completa

Consulta `API_DOCUMENTACION.md` para la documentación completa de todos los endpoints.

