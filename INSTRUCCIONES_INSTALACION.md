# 📋 Instrucciones de Instalación - Windows

## Pasos a seguir desde el CMD o PowerShell

### 1. Abrir CMD o PowerShell y navegar a la carpeta del proyecto

```cmd
cd "C:\Kevin trabajos\actividad_django_web-main\actividades_django_web"
```

### 2. (Opcional pero recomendado) Crear y activar entorno virtual

```cmd
python -m venv venv
venv\Scripts\activate
```

> **Nota:** Si ves `(venv)` al inicio de la línea, el entorno virtual está activado.

### 3. Instalar Django

```cmd
pip install -r requirements.txt
```

### 4. Crear las migraciones

```cmd
python manage.py makemigrations
```

Deberías ver algo como:
```
Migrations for 'biblioteca':
  biblioteca\migrations\0001_initial.py
    - Create model Autor
    - Create model Libro
    - Create model Resena
```

### 5. Aplicar las migraciones a la base de datos

```cmd
python manage.py migrate
```

### 6. Crear un superusuario (para acceder al panel de administración)

```cmd
python manage.py createsuperuser
```

Te pedirá:
- Username (nombre de usuario)
- Email address (opcional, puedes presionar Enter)
- Password (contraseña - no se verá mientras escribes)
- Password (again) (confirmar contraseña)

### 7. Poblar datos iniciales (opcional pero recomendado)

```cmd
python biblioteca\poblar_datos.py
```

O si prefieres usar la shell de Django:

```cmd
python manage.py shell
```

Luego dentro de la shell:
```python
from biblioteca.poblar_datos import poblar_datos
poblar_datos()
exit()
```

### 8. Ejecutar el servidor de desarrollo

```cmd
python manage.py runserver
```

Deberías ver:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 9. Abrir en el navegador

- **Página principal (lista de libros):** http://127.0.0.1:8000/
- **Panel de administración:** http://127.0.0.1:8000/admin/

## ✅ Resumen de comandos (en orden)

```cmd
cd "C:\Kevin trabajos\actividad_django_web-main\actividades_django_web"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python biblioteca\poblar_datos.py
python manage.py runserver
```

## 🔧 Solución de problemas comunes

### Error: "python no se reconoce como comando"
- Usa `py` en lugar de `python`:
  ```cmd
  py manage.py migrate
  ```

### Error: "No module named 'django'"
- Asegúrate de haber activado el entorno virtual (deberías ver `(venv)` al inicio)
- O instala Django globalmente: `pip install django`

### Error al ejecutar poblar_datos.py
- Asegúrate de haber ejecutado las migraciones primero
- O usa la shell de Django como alternativa

## 🎯 ¿Listo?

Una vez que el servidor esté corriendo, podrás:
- Ver los libros en: http://127.0.0.1:8000/
- Administrar datos en: http://127.0.0.1:8000/admin/
- Ver autores en: http://127.0.0.1:8000/autores/

