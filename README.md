# Biblioteca Django - Proyecto Web

Aplicación web Django para gestionar una biblioteca con autores, libros y reseñas.

## Características

- ✅ Registro de autores y libros
- ✅ Sistema de reseñas para cada libro
- ✅ Visualización de libros y sus reseñas
- ✅ Panel de administración personalizado
- ✅ Validaciones personalizadas en los modelos
- ✅ Script para poblar datos iniciales

## Estructura del Proyecto

```
actividades_django_web/
├── actividades_django_web/    # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── biblioteca/                # App principal
│   ├── models.py             # Modelos: Autor, Libro, Resena
│   ├── admin.py              # Configuración del admin
│   ├── views.py              # Vistas para visualizar libros
│   ├── urls.py               # URLs de la app
│   ├── poblar_datos.py       # Script para poblar datos
│   └── templates/            # Plantillas HTML
└── manage.py
```

## Instalación

1. **Crear y activar un entorno virtual** (recomendado):

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

2. **Instalar dependencias**:

```bash
pip install -r requirements.txt
```

3. **Aplicar migraciones**:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Crear un superusuario** (para acceder al panel de administración):

```bash
python manage.py createsuperuser
```

5. **Poblar datos iniciales** (opcional):

```bash
python biblioteca/poblar_datos.py
```

O desde la shell de Django:

```bash
python manage.py shell
```

```python
from biblioteca.poblar_datos import poblar_datos
poblar_datos()
```

6. **Ejecutar el servidor de desarrollo**:

```bash
python manage.py runserver
```

7. **Acceder a la aplicación**:

- Página principal: http://127.0.0.1:8000/
- Panel de administración: http://127.0.0.1:8000/admin/

## Modelos

### Autor
- `nombre`: CharField (validación: no puede estar vacío o contener solo espacios)
- `nacionalidad`: CharField

### Libro
- `titulo`: CharField
- `autor`: ForeignKey a Autor
- `fecha_publicacion`: DateField
- `resumen`: TextField (validación: mínimo 50 caracteres)

### Resena
- `libro`: ForeignKey a Libro
- `texto`: TextField
- `calificacion`: IntegerField (validación: entre 1 y 5)
- `fecha`: DateTimeField (se establece automáticamente)

## Validaciones Personalizadas

El proyecto incluye validadores personalizados:

1. **Autor**: Valida que el nombre no esté vacío o contenga solo espacios
2. **Libro**: Valida que el resumen tenga al menos 50 caracteres
3. **Resena**: Valida que la calificación esté entre 1 y 5

## Panel de Administración

El panel de administración incluye:

- **AutorAdmin**: Búsqueda por nombre y nacionalidad, filtros, muestra cantidad de libros
- **LibroAdmin**: Búsqueda por título y autor, filtros, muestra cantidad de reseñas y calificación promedio
- **ResenaAdmin**: Búsqueda por libro y texto, filtros por calificación y fecha

## URLs Disponibles

- `/` - Lista de libros
- `/libros/` - Lista de libros
- `/libros/<id>/` - Detalle de un libro con sus reseñas
- `/autores/` - Lista de autores
- `/admin/` - Panel de administración

## Uso del Script de Población de Datos

El script `poblar_datos.py` crea:

- 4 autores (Gabriel García Márquez, Isabel Allende, Mario Vargas Llosa, Julio Cortázar)
- 6 libros de estos autores
- 9 reseñas distribuidas entre los libros

Para ejecutarlo:

```bash
python biblioteca/poblar_datos.py
```

## Tecnologías Utilizadas

- Django 5.2.8
- Python 3.x
- SQLite (base de datos por defecto)

## Autor

Proyecto desarrollado como actividad de aprendizaje de Django.

