# poblar_datos.py
from datetime import date


def poblar_datos():
    # Importar después de configurar Django
    from biblioteca.models import Autor, Libro, Resena
    from django.utils import timezone
    """Función para poblar la base de datos con datos iniciales"""
    
    # Crear autores
    print("Creando autores...")
    autor1 = Autor.objects.create(
        nombre="Gabriel García Márquez",
        nacionalidad="Colombiana"
    )
    autor2 = Autor.objects.create(
        nombre="Isabel Allende",
        nacionalidad="Chilena"
    )
    autor3 = Autor.objects.create(
        nombre="Mario Vargas Llosa",
        nacionalidad="Peruana"
    )
    autor4 = Autor.objects.create(
        nombre="Julio Cortázar",
        nacionalidad="Argentina"
    )
    print(f"✓ Creados {Autor.objects.count()} autores")
    
    # Crear libros
    print("\nCreando libros...")
    libro1 = Libro.objects.create(
        titulo="Cien años de soledad",
        autor=autor1,
        fecha_publicacion=date(1967, 6, 5),
        resumen="Novela emblemática del realismo mágico que narra la historia de la familia Buendía a lo largo de siete generaciones en el pueblo ficticio de Macondo."
    )
    
    libro2 = Libro.objects.create(
        titulo="El amor en los tiempos del cólera",
        autor=autor1,
        fecha_publicacion=date(1985, 1, 1),
        resumen="Historia de amor que se desarrolla a lo largo de más de cincuenta años, mostrando cómo el amor puede perdurar a través del tiempo y las adversidades."
    )
    
    libro3 = Libro.objects.create(
        titulo="La casa de los espíritus",
        autor=autor2,
        fecha_publicacion=date(1982, 1, 1),
        resumen="Primera novela de Isabel Allende que narra la saga de la familia Trueba a lo largo de cuatro generaciones, combinando elementos de realismo mágico con la historia política de Chile."
    )
    
    libro4 = Libro.objects.create(
        titulo="Eva Luna",
        autor=autor2,
        fecha_publicacion=date(1987, 1, 1),
        resumen="Historia de una joven que crece en un país latinoamericano sin nombre, contando historias que la ayudan a sobrevivir y encontrar su lugar en el mundo."
    )
    
    libro5 = Libro.objects.create(
        titulo="La ciudad y los perros",
        autor=autor3,
        fecha_publicacion=date(1963, 1, 1),
        resumen="Primera novela de Vargas Llosa que explora la vida en un colegio militar de Lima, mostrando la violencia y la corrupción que existe en la sociedad peruana."
    )
    
    libro6 = Libro.objects.create(
        titulo="Rayuela",
        autor=autor4,
        fecha_publicacion=date(1963, 6, 28),
        resumen="Novela experimental que puede leerse de dos formas diferentes, siguiendo el orden tradicional o el orden propuesto por el autor, explorando temas como el amor, la búsqueda de sentido y la identidad."
    )
    
    print(f"✓ Creados {Libro.objects.count()} libros")
    
    # Crear reseñas
    print("\nCreando reseñas...")
    
    # Reseñas para Cien años de soledad
    Resena.objects.create(
        libro=libro1,
        texto="Una obra maestra de la literatura latinoamericana. García Márquez crea un mundo mágico y realista que atrapa desde la primera página. La narrativa es fluida y los personajes son inolvidables.",
        calificacion=5,
        rating=4.9,
        fecha=timezone.now()
    )
    
    Resena.objects.create(
        libro=libro1,
        texto="Excelente novela, aunque puede resultar compleja por la cantidad de personajes con nombres similares. El realismo mágico está presente en cada página.",
        calificacion=4,
        rating=4.2,
        fecha=timezone.now()
    )
    
    # Reseñas para El amor en los tiempos del cólera
    Resena.objects.create(
        libro=libro2,
        texto="Una historia de amor conmovedora que muestra la paciencia y la perseverancia. La prosa de García Márquez es exquisita y cada página está llena de poesía.",
        calificacion=5,
        rating=4.8,
        fecha=timezone.now()
    )
    
    # Reseñas para La casa de los espíritus
    Resena.objects.create(
        libro=libro3,
        texto="Una saga familiar fascinante que combina elementos mágicos con la realidad política. Isabel Allende demuestra su maestría narrativa desde su primera novela.",
        calificacion=5,
        rating=4.7,
        fecha=timezone.now()
    )
    
    Resena.objects.create(
        libro=libro3,
        texto="Buen libro, aunque algunos pasajes pueden ser un poco lentos. Los personajes femeninos están muy bien desarrollados.",
        calificacion=4,
        rating=4.0,
        fecha=timezone.now()
    )
    
    # Reseñas para Eva Luna
    Resena.objects.create(
        libro=libro4,
        texto="Una historia encantadora sobre el poder de las historias. La protagonista es memorable y la narrativa fluye de manera natural.",
        calificacion=4,
        rating=4.1,
        fecha=timezone.now()
    )
    
    # Reseñas para La ciudad y los perros
    Resena.objects.create(
        libro=libro5,
        texto="Una novela dura y realista que muestra las consecuencias de la violencia institucionalizada. Vargas Llosa es un maestro de la narrativa.",
        calificacion=5,
        rating=4.6,
        fecha=timezone.now()
    )
    
    # Reseñas para Rayuela
    Resena.objects.create(
        libro=libro6,
        texto="Una obra experimental fascinante. La posibilidad de leerla de dos formas diferentes la hace única. Requiere atención y paciencia, pero vale la pena.",
        calificacion=4,
        rating=4.3,
        fecha=timezone.now()
    )
    
    Resena.objects.create(
        libro=libro6,
        texto="Libro complejo pero innovador. La estructura no lineal puede desconcertar al principio, pero una vez que te acostumbras, es una experiencia literaria única.",
        calificacion=4,
        rating=4.2,
        fecha=timezone.now()
    )
    
    print(f"✓ Creadas {Resena.objects.count()} reseñas")
    
    print("\n" + "="*50)
    print("¡Datos poblados exitosamente!")
    print("="*50)
    print(f"\nResumen:")
    print(f"- Autores: {Autor.objects.count()}")
    print(f"- Libros: {Libro.objects.count()}")
    print(f"- Reseñas: {Resena.objects.count()}")


if __name__ == "__main__":
    import os
    import sys
    import django
    
    # Agregar el directorio padre al path para que Python encuentre el módulo del proyecto
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, BASE_DIR)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'actividades_django_web.settings')
    django.setup()
    
    poblar_datos()

