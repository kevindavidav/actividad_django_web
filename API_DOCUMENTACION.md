# 📚 Documentación de la API REST - Biblioteca

Esta documentación describe los endpoints disponibles en la API REST de la aplicación Biblioteca.

## 🔗 Base URL

```
http://127.0.0.1:8000/api/
```

## 📋 Endpoints Disponibles

### 1. Autores (Authors)

#### Listar todos los autores
```
GET /api/authors/
```

**Parámetros de consulta:**
- `search`: Búsqueda en nombre y nacionalidad
- `ordering`: Ordenamiento (nombre, nacionalidad)
- `nacionalidad`: Filtrar por nacionalidad
- `page`: Número de página (paginación)

**Ejemplo:**
```
GET /api/authors/?search=García&ordering=nombre
```

#### Obtener un autor específico
```
GET /api/authors/{id}/
```

#### Crear un nuevo autor
```
POST /api/authors/
Content-Type: application/json

{
    "nombre": "Gabriel García Márquez",
    "nacionalidad": "Colombiana"
}
```

#### Actualizar un autor
```
PUT /api/authors/{id}/
PATCH /api/authors/{id}/
```

#### Eliminar un autor
```
DELETE /api/authors/{id}/
```

#### Ruta personalizada: Libros de un autor
```
GET /api/authors/{id}/libros/
```

Retorna todos los libros de un autor específico.

---

### 2. Libros (Books)

#### Listar todos los libros
```
GET /api/books/
```

**Parámetros de consulta:**
- `author`: Filtrar por ID de autor
- `year`: Filtrar por año de publicación
- `search`: Búsqueda en título, resumen y nombre del autor
- `ordering`: Ordenamiento (titulo, fecha_publicacion, -publication_year)
- `page`: Número de página

**Ejemplos:**
```
GET /api/books/?author=2
GET /api/books/?ordering=-publication_year
GET /api/books/?page=2
GET /api/books/?author=1&ordering=-fecha_publicacion
```

#### Obtener un libro específico
```
GET /api/books/{id}/
```

Retorna el libro con información detallada del autor y las 5 reseñas más recientes.

#### Crear un nuevo libro
```
POST /api/books/
Content-Type: application/json

{
    "titulo": "Cien años de soledad",
    "autor": 1,
    "fecha_publicacion": "1967-06-05",
    "resumen": "Novela emblemática del realismo mágico que narra la historia de la familia Buendía a lo largo de siete generaciones en el pueblo ficticio de Macondo."
}
```

#### Actualizar un libro
```
PUT /api/books/{id}/
PATCH /api/books/{id}/
```

#### Eliminar un libro
```
DELETE /api/books/{id}/
```

#### Ruta personalizada: Rating promedio
```
GET /api/books/{id}/rating_promedio/
```

Retorna el rating promedio de un libro basado en las reseñas.

**Respuesta:**
```json
{
    "libro_id": 1,
    "titulo": "Cien años de soledad",
    "rating_promedio": 4.5,
    "total_resenas": 2,
    "resenas_con_rating": 2
}
```

#### Ruta personalizada: Libros por autor
```
GET /api/books/por_autor/?autor_id=1
```

Retorna todos los libros de un autor específico.

---

### 3. Reseñas (Reviews)

#### Listar todas las reseñas
```
GET /api/reviews/
```

**Parámetros de consulta:**
- `libro`: Filtrar por ID de libro
- `calificacion`: Filtrar por calificación (1-5)
- `rating_min`: Filtrar por rating mínimo (0.0-5.0)
- `rating_max`: Filtrar por rating máximo (0.0-5.0)
- `search`: Búsqueda en texto y título del libro
- `ordering`: Ordenamiento (fecha, calificacion, rating)
- `page`: Número de página

**Ejemplos:**
```
GET /api/reviews/?libro=1
GET /api/reviews/?rating_min=4.0&rating_max=5.0
GET /api/reviews/?ordering=-fecha
```

#### Obtener una reseña específica
```
GET /api/reviews/{id}/
```

#### Crear una nueva reseña
```
POST /api/reviews/
Content-Type: application/json

{
    "libro": 1,
    "texto": "Una obra maestra de la literatura latinoamericana.",
    "calificacion": 5,
    "rating": 4.8
}
```

**Nota:** Si no se proporciona `rating`, se usará `calificacion` como valor base.

#### Actualizar una reseña
```
PUT /api/reviews/{id}/
PATCH /api/reviews/{id}/
```

#### Eliminar una reseña
```
DELETE /api/reviews/{id}/
```

---

## 🔍 Características de los Serializadores

### AutorSerializer
- `id`: ID del autor
- `nombre`: Nombre del autor
- `nacionalidad`: Nacionalidad del autor
- `cantidad_libros`: Campo computado que muestra la cantidad de libros del autor

### LibroSerializer
- `id`: ID del libro
- `titulo`: Título del libro
- `autor`: ID del autor (ForeignKey)
- `author_name`: Campo ReadOnly que muestra el nombre del autor
- `fecha_publicacion`: Fecha de publicación
- `year`: Campo computado que muestra el año de publicación
- `resumen`: Resumen del libro
- `recent_reviews`: Campo SerializerMethodField que muestra las 5 reseñas más recientes
- `rating_promedio`: Campo computado que muestra el rating promedio del libro

### LibroDetailSerializer
Extiende `LibroSerializer` e incluye:
- `autor`: Objeto completo del autor (serializado con AutorSerializer)

### ResenaSerializer
- `id`: ID de la reseña
- `libro`: ID del libro (ForeignKey)
- `texto`: Texto de la reseña
- `calificacion`: Calificación del 1 al 5 (IntegerField)
- `rating`: Rating del 0.0 al 5.0 (FloatField con validadores)
- `fecha`: Fecha de la reseña (automática)

---

## ✅ Validaciones

### Modelo Resena
- `rating`: Debe estar entre 0.0 y 5.0 (usando MinValueValidator y MaxValueValidator)
- `calificacion`: Debe estar entre 1 y 5 (validador personalizado)

### Modelo Autor
- `nombre`: No puede estar vacío o contener solo espacios

### Modelo Libro
- `resumen`: Debe tener al menos 50 caracteres

---

## 📄 Paginación

La API utiliza paginación por defecto con 10 elementos por página.

**Ejemplo de respuesta paginada:**
```json
{
    "count": 25,
    "next": "http://127.0.0.1:8000/api/books/?page=2",
    "previous": null,
    "results": [...]
}
```

---

## 🧪 Ejemplos de Uso

### Ejemplo 1: Obtener libros de un autor específico
```bash
GET /api/books/?author=1
```

### Ejemplo 2: Obtener libros ordenados por año (más recientes primero)
```bash
GET /api/books/?ordering=-publication_year
```

### Ejemplo 3: Obtener reseñas con rating entre 4.0 y 5.0
```bash
GET /api/reviews/?rating_min=4.0&rating_max=5.0
```

### Ejemplo 4: Crear una nueva reseña
```bash
POST /api/reviews/
Content-Type: application/json

{
    "libro": 1,
    "texto": "Excelente novela, muy recomendada.",
    "calificacion": 5,
    "rating": 4.9
}
```

### Ejemplo 5: Obtener rating promedio de un libro
```bash
GET /api/books/1/rating_promedio/
```

---

## 🛠️ Herramientas para Probar la API

1. **Navegador**: Accede a http://127.0.0.1:8000/api/ para ver la interfaz Browsable API
2. **Postman**: Importa los endpoints y prueba las peticiones
3. **Insomnia**: Similar a Postman, permite probar la API
4. **curl**: Desde la línea de comandos

### Ejemplo con curl:
```bash
# Obtener todos los libros
curl http://127.0.0.1:8000/api/books/

# Crear un nuevo autor
curl -X POST http://127.0.0.1:8000/api/authors/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Nuevo Autor", "nacionalidad": "Española"}'
```

---

## 📝 Notas Importantes

1. El campo `rating` en Resena es opcional (puede ser null)
2. Si no se proporciona `rating` al crear una reseña, se usará `calificacion` como valor base
3. El campo `year` en Libro es una propiedad calculada, no se puede modificar directamente
4. Las rutas personalizadas están disponibles en los ViewSets correspondientes
5. Todos los endpoints soportan la interfaz Browsable API de DRF

---

## 🔐 Autenticación

Actualmente la API no requiere autenticación. Para producción, se recomienda implementar:
- Token Authentication
- Session Authentication
- OAuth2

