from django.core.management.base import BaseCommand
from crud_app.models import Categoria

class Command(BaseCommand):
    help = 'Crea las categorías predefinidas para el ecommerce'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Elimina todas las categorías existentes antes de crear las nuevas',
        )

    def handle(self, *args, **options):
        if options['limpiar']:
            count = Categoria.objects.all().count()
            Categoria.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f'✓ Se eliminaron {count} categorías existentes')
            )

        categorias_data = [
            {
                'nombre': 'Laptops Gaming',
                'descripcion': 'Laptops de alto rendimiento diseñadas para gaming con procesadores potentes, tarjetas gráficas dedicadas y pantallas de alta frecuencia de actualización.',
                'icono': '🎮',
                'orden': 1
            },
            {
                'nombre': 'Laptops Profesionales',
                'descripcion': 'Equipos portátiles premium para profesionales, con pantallas de alta calidad, gran autonomía y excelente rendimiento para trabajo intensivo.',
                'icono': '💼',
                'orden': 2
            },
            {
                'nombre': 'Laptops Ultraportátiles',
                'descripcion': 'Portátiles ultraligeros y compactos, ideales para movilidad con gran autonomía de batería y diseño delgado.',
                'icono': '✈️',
                'orden': 3
            },
            {
                'nombre': 'PC Gaming',
                'descripcion': 'Computadores de escritorio potentes para juegos con las últimas tecnologías en procesadores y tarjetas gráficas.',
                'icono': '🖥️',
                'orden': 4
            },
            {
                'nombre': 'PC Oficina',
                'descripcion': 'Equipos de escritorio ideales para tareas de oficina, productividad y uso general con excelente relación precio-rendimiento.',
                'icono': '🏢',
                'orden': 5
            },
            {
                'nombre': 'Monitores',
                'descripcion': 'Pantallas de alta calidad para gaming, diseño y productividad con diversas tecnologías de panel y resoluciones.',
                'icono': '🖼️',
                'orden': 6
            },
            {
                'nombre': 'Accesorios',
                'descripcion': 'Periféricos y accesorios para mejorar tu setup: teclados, ratones, auriculares y más.',
                'icono': '⌨️',
                'orden': 7
            },
        ]

        categorias_creadas = 0
        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={
                    'descripcion': cat_data['descripcion'],
                    'icono': cat_data['icono'],
                    'orden': cat_data['orden'],
                    'activa': True
                }
            )
            
            if created:
                categorias_creadas += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Categoría creada: {categoria}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'• Categoría ya existe: {categoria}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Proceso completado: {categorias_creadas} nuevas categorías creadas')
        )
