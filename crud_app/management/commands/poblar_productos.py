"""
Comando personalizado de Django para poblar la base de datos con productos
Ejecutar con: python manage.py poblar_productos
IMPORTANTE: Primero ejecutar python manage.py poblar_categorias
"""

from django.core.management.base import BaseCommand
from crud_app.models import Producto, Categoria
from django.db.models import Count


class Command(BaseCommand):
    help = 'Pobla la base de datos con productos de tecnología de ejemplo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Eliminar todos los productos existentes antes de poblar',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🚀 Iniciando población de productos...\n'))

        # Verificar que existan las categorías necesarias
        categorias_necesarias = [
            'Laptops Gaming', 'Laptops Profesionales', 'Laptops Ultraportátiles',
            'PC Gaming', 'PC Oficina', 'Monitores', 'Accesorios'
        ]
        
        categorias_faltantes = []
        for cat_nombre in categorias_necesarias:
            if not Categoria.objects.filter(nombre=cat_nombre).exists():
                categorias_faltantes.append(cat_nombre)
        
        if categorias_faltantes:
            self.stdout.write(
                self.style.ERROR(
                    f'\n⚠️  ERROR: Faltan las siguientes categorías:\n'
                    f'   {", ".join(categorias_faltantes)}\n'
                    f'\n   Ejecuta primero: python manage.py poblar_categorias\n'
                )
            )
            return

        if options['limpiar']:
            count = Producto.objects.count()
            Producto.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'🗑️  Se eliminaron {count} productos existentes\n'))

        productos = self.get_productos_data()
        
        productos_creados = 0
        productos_actualizados = 0

        for prod_data in productos:
            # Buscar la categoría correspondiente
            try:
                categoria = Categoria.objects.get(nombre=prod_data['categoria'])
            except Categoria.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'✗ Categoría no encontrada: {prod_data["categoria"]} para {prod_data["nombre"]}')
                )
                continue

            # Guardar el nombre de categoría en categoria_texto para compatibilidad
            categoria_texto = prod_data['categoria']
            
            # Remover 'categoria' del dict para usar categoria_fk
            prod_data_copy = prod_data.copy()
            prod_data_copy.pop('categoria')
            prod_data_copy['categoria_texto'] = categoria_texto
            prod_data_copy['categoria_fk'] = categoria

            producto, created = Producto.objects.get_or_create(
                nombre=prod_data['nombre'],
                defaults=prod_data_copy
            )
            
            if created:
                productos_creados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creado: {producto.nombre} - ${producto.precio} ({categoria.icono} {categoria.nombre})')
                )
            else:
                for key, value in prod_data_copy.items():
                    setattr(producto, key, value)
                producto.save()
                productos_actualizados += 1
                self.stdout.write(
                    self.style.HTTP_INFO(f'↻ Actualizado: {producto.nombre} - ${producto.precio}')
                )

        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS(f'✨ Resumen:'))
        self.stdout.write(f'   • Productos creados: {productos_creados}')
        self.stdout.write(f'   • Productos actualizados: {productos_actualizados}')
        self.stdout.write(f'   • Total en base de datos: {Producto.objects.count()}')
        self.stdout.write('='*70 + '\n')
        
        self.stdout.write(self.style.SUCCESS('📊 Productos por categoría:'))
        # Usar categoria_fk en lugar de categoria
        for categoria in Categoria.objects.all():
            count = categoria.productos.count()
            if count > 0:
                self.stdout.write(f"   • {categoria.icono} {categoria.nombre}: {count} productos")
        
        self.stdout.write(self.style.SUCCESS('\n✅ ¡Base de datos poblada exitosamente!\n'))

    def get_productos_data(self):
        """Retorna la lista de productos para poblar"""
        return [
            # ========== LAPTOPS GAMING ==========
            {
                'nombre': 'ASUS ROG Strix G16',
                'descripcion': 'Laptop gaming de alto rendimiento con procesador Intel Core i7 de 13ª generación y GPU NVIDIA RTX 4060. Perfecta para gaming competitivo y creación de contenido con pantalla de 165Hz.',
                'precio': 1499.99,
                'marca': 'ASUS',
                'categoria': 'Laptops Gaming',
                'especificaciones': '''• Procesador: Intel Core i7-13650HX (hasta 4.9 GHz)
• GPU: NVIDIA GeForce RTX 4060 8GB GDDR6
• RAM: 16GB DDR5 4800MHz (expandible a 32GB)
• Almacenamiento: 512GB NVMe SSD
• Pantalla: 16" FHD (1920x1200) 165Hz
• Teclado: RGB por tecla
• Conectividad: Wi-Fi 6E, Bluetooth 5.2
• Puertos: USB-C Thunderbolt 4, HDMI 2.1, RJ45
• Batería: 90Wh
• Peso: 2.5 kg''',
                'stock': 8
            },
            {
                'nombre': 'MSI Katana 15',
                'descripcion': 'Portátil gaming con diseño inspirado en samuráis. Equipado con RTX 4050 y procesador Intel de última generación, ideal para juegos AAA y multitarea exigente.',
                'precio': 1199.99,
                'marca': 'MSI',
                'categoria': 'Laptops Gaming',
                'especificaciones': '''• Procesador: Intel Core i7-13620H (10 núcleos)
• GPU: NVIDIA GeForce RTX 4050 6GB
• RAM: 16GB DDR5 5200MHz
• Almacenamiento: 1TB NVMe SSD
• Pantalla: 15.6" FHD 144Hz IPS
• Sistema de refrigeración: Cooler Boost 5
• Audio: Nahimic 3
• Conectividad: Wi-Fi 6, Bluetooth 5.3
• Puertos: USB-C, HDMI 2.1, Mini DisplayPort
• Peso: 2.25 kg''',
                'stock': 12
            },
            {
                'nombre': 'Lenovo Legion 5 Pro',
                'descripcion': 'Laptop gaming premium con procesador AMD Ryzen y pantalla QHD de alto refresh rate. Diseño sobrio perfecto para gaming y trabajo profesional.',
                'precio': 1699.99,
                'marca': 'Lenovo',
                'categoria': 'Laptops Gaming',
                'especificaciones': '''• Procesador: AMD Ryzen 7 7745HX (8 núcleos)
• GPU: NVIDIA GeForce RTX 4070 8GB
• RAM: 32GB DDR5 4800MHz
• Almacenamiento: 1TB PCIe Gen 4 SSD
• Pantalla: 16" QHD (2560x1600) 240Hz
• TGP GPU: 140W
• Teclado: RGB 4 zonas
• Sistema de refrigeración: Legion Coldfront 5.0
• Batería: 80Wh
• Peso: 2.4 kg''',
                'stock': 5
            },
            
            # ========== LAPTOPS PROFESIONALES ==========
            {
                'nombre': 'Dell XPS 15 9530',
                'descripcion': 'Ultrabook premium con pantalla OLED 4K táctil. Ideal para profesionales creativos, editores de video y diseñadores que buscan máxima portabilidad sin sacrificar rendimiento.',
                'precio': 2199.99,
                'marca': 'Dell',
                'categoria': 'Laptops Profesionales',
                'especificaciones': '''• Procesador: Intel Core i7-13700H (14 núcleos)
• GPU: NVIDIA GeForce RTX 4050 6GB
• RAM: 16GB DDR5 4800MHz
• Almacenamiento: 512GB PCIe Gen 4 SSD
• Pantalla: 15.6" OLED 4K (3840x2400) táctil
• Cobertura de color: 100% DCI-P3
• Construcción: Aluminio mecanizado CNC
• Batería: 86Wh (hasta 13 horas)
• Peso: 1.86 kg
• Windows 11 Pro''',
                'stock': 7
            },
            {
                'nombre': 'HP Spectre x360 14',
                'descripcion': 'Convertible 2-en-1 con bisagra de 360°. Perfecta para profesionales que necesitan versatilidad. Incluye lápiz óptico y diseño ultradelgado con certificación Intel Evo.',
                'precio': 1599.99,
                'marca': 'HP',
                'categoria': 'Laptops Profesionales',
                'especificaciones': '''• Procesador: Intel Core i7-1355U (10 núcleos)
• GPU: Intel Iris Xe Graphics
• RAM: 16GB LPDDR4x
• Almacenamiento: 1TB PCIe NVMe SSD
• Pantalla: 13.5" OLED 3K2K táctil
• Lápiz HP Rechargeable Tilt Pen incluido
• Batería: 66Wh (hasta 17 horas)
• Conectividad: Wi-Fi 6E, Thunderbolt 4
• Bang & Olufsen audio
• Peso: 1.34 kg''',
                'stock': 10
            },
            {
                'nombre': 'MacBook Pro 14" M3 Pro',
                'descripcion': 'La potencia del chip M3 Pro de Apple en un diseño compacto. Ideal para desarrolladores, editores de video y profesionales creativos. Pantalla Liquid Retina XDR con ProMotion.',
                'precio': 2499.99,
                'marca': 'Apple',
                'categoria': 'Laptops Profesionales',
                'especificaciones': '''• Chip: Apple M3 Pro (11 núcleos CPU, 14 núcleos GPU)
• Neural Engine de 16 núcleos
• RAM: 18GB Memoria Unificada
• Almacenamiento: 512GB SSD
• Pantalla: 14.2" Liquid Retina XDR (3024x1964)
• ProMotion hasta 120Hz
• Brightness: 1600 nits pico (HDR)
• Cámara: FaceTime HD 1080p
• Puertos: 3x Thunderbolt 4, HDMI, SD
• Batería: hasta 18 horas
• Peso: 1.6 kg
• macOS Sonoma''',
                'stock': 6
            },
            
            # ========== LAPTOPS ULTRAPORTÁTILES ==========
            {
                'nombre': 'ASUS ZenBook 14 OLED',
                'descripcion': 'Ultrabook elegante y ligero con pantalla OLED vibrante. Perfecta para profesionales móviles, estudiantes y viajeros frecuentes. Diseño premium a precio accesible.',
                'precio': 899.99,
                'marca': 'ASUS',
                'categoria': 'Laptops Ultraportátiles',
                'especificaciones': '''• Procesador: Intel Core i7-1355U
• GPU: Intel Iris Xe Graphics
• RAM: 16GB LPDDR5
• Almacenamiento: 512GB PCIe 4.0 SSD
• Pantalla: 14" 2.8K (2880x1800) OLED
• 90Hz, 100% DCI-P3, Pantone Validated
• Batería: 75Wh (hasta 15 horas)
• Carga rápida: 60% en 49 min
• Peso: 1.39 kg
• Grosor: 16.9 mm
• Windows 11 Home''',
                'stock': 15
            },
            {
                'nombre': 'LG Gram 17',
                'descripcion': 'La laptop de 17 pulgadas más ligera del mundo. Batería de larga duración y gran pantalla para productividad máxima sin sacrificar portabilidad.',
                'precio': 1799.99,
                'marca': 'LG',
                'categoria': 'Laptops Ultraportátiles',
                'especificaciones': '''• Procesador: Intel Core i7-1360P (12 núcleos)
• GPU: Intel Iris Xe Graphics
• RAM: 16GB LPDDR5
• Almacenamiento: 1TB NVMe SSD
• Pantalla: 17" WQXGA (2560x1600) IPS
• Batería: 80Wh (hasta 20 horas)
• Construcción: Aleación nano-carbono + magnesio
• Certificación militar MIL-STD-810H
• Peso: solo 1.35 kg
• Grosor: 17.8 mm''',
                'stock': 4
            },
            
            # ========== COMPUTADORAS DE ESCRITORIO ==========
            {
                'nombre': 'PC Gaming RGB Elite',
                'descripcion': 'Computadora gaming ensamblada con componentes de alta gama. RTX 4070 Ti y procesador Intel Core i7. Case con ventiladores RGB y sistema de refrigeración líquida.',
                'precio': 2299.99,
                'marca': 'Custom Build',
                'categoria': 'PC Gaming',
                'especificaciones': '''• Procesador: Intel Core i7-13700K (16 núcleos)
• GPU: NVIDIA RTX 4070 Ti 12GB
• RAM: 32GB DDR5 6000MHz (2x16GB)
• Almacenamiento: 1TB NVMe Gen 4 + 2TB HDD
• Motherboard: ASUS ROG STRIX Z790
• Refrigeración: AIO 240mm RGB
• Fuente: 850W 80+ Gold Modular
• Case: NZXT H510 Elite con ventiladores RGB
• Wi-Fi 6E incluido
• Windows 11 Pro''',
                'stock': 3
            },
            {
                'nombre': 'Dell Optiplex 7010 Tower',
                'descripcion': 'PC de escritorio profesional para oficina. Confiable, expandible y con soporte empresarial. Ideal para empresas que buscan computadoras duraderas.',
                'precio': 799.99,
                'marca': 'Dell',
                'categoria': 'PC Oficina',
                'especificaciones': '''• Procesador: Intel Core i5-13500 (14 núcleos)
• GPU: Intel UHD Graphics 770
• RAM: 16GB DDR4 3200MHz
• Almacenamiento: 512GB NVMe SSD
• Unidad óptica: DVD±RW
• Conectividad: Wi-Fi 6, Bluetooth 5.2
• Puertos: 10x USB (2x USB-C), DisplayPort, HDMI
• Fuente: 260W
• Garantía: 3 años on-site
• Windows 11 Pro''',
                'stock': 20
            },
            {
                'nombre': 'Apple Mac Mini M2 Pro',
                'descripcion': 'Computadora de escritorio compacta con el poder del chip M2 Pro. Perfecta para estudios de diseño, edición de video 8K y desarrollo de software.',
                'precio': 1399.99,
                'marca': 'Apple',
                'categoria': 'PC Oficina',
                'especificaciones': '''• Chip: Apple M2 Pro (12 núcleos CPU, 19 GPU)
• Neural Engine de 16 núcleos
• RAM: 16GB Memoria Unificada
• Almacenamiento: 512GB SSD
• Conectividad: Wi-Fi 6E, Bluetooth 5.3, Ethernet 10Gb
• Puertos: 4x Thunderbolt 4, 2x USB-A, HDMI
• Soporte hasta 3 pantallas
• Dimensiones: 19.7 x 19.7 x 3.6 cm
• Peso: 1.28 kg
• macOS Sonoma''',
                'stock': 9
            },
            
            # ========== MONITORES ==========
            {
                'nombre': 'LG UltraGear 27" 4K Gaming',
                'descripcion': 'Monitor gaming 4K con 144Hz y tiempo de respuesta de 1ms. Compatible con NVIDIA G-SYNC y AMD FreeSync Premium Pro. Ideal para gaming en ultra definición.',
                'precio': 599.99,
                'marca': 'LG',
                'categoria': 'Monitores',
                'especificaciones': '''• Tamaño: 27" (68.6 cm)
• Resolución: 4K UHD (3840x2160)
• Tasa de refresco: 144Hz
• Tiempo de respuesta: 1ms (GtG)
• Panel: Nano IPS
• HDR: VESA DisplayHDR 600
• Cobertura: 98% DCI-P3
• G-SYNC & FreeSync Premium Pro
• Puertos: 2x HDMI 2.1, DisplayPort 1.4, USB-C
• Soporte ajustable (altura, pivot, tilt)''',
                'stock': 12
            },
            {
                'nombre': 'Samsung Odyssey G7 32" Curvo',
                'descripcion': 'Monitor gaming curvo ultrainmersivo con 240Hz. Curvatura 1000R y panel QLED para colores vibrantes. El monitor perfecto para simuladores y FPS competitivos.',
                'precio': 749.99,
                'marca': 'Samsung',
                'categoria': 'Monitores',
                'especificaciones': '''• Tamaño: 32" curvo (1000R)
• Resolución: QHD (2560x1440)
• Tasa de refresco: 240Hz
• Tiempo de respuesta: 1ms (MPRT)
• Panel: VA QLED
• HDR: HDR600
• G-SYNC & FreeSync Premium Pro
• Infinity Core Lighting RGB
• Eye Saver Mode & Flicker Free
• Puertos: 2x HDMI 2.0, DisplayPort 1.4, USB Hub
• Soporte ajustable completo''',
                'stock': 8
            },
            
            # ========== ACCESORIOS ==========
            {
                'nombre': 'Logitech MX Master 3S',
                'descripcion': 'Mouse inalámbrico ergonómico premium para profesionales. Sensor de 8000 DPI, batería de larga duración y diseño ergonómico perfecto para largas jornadas.',
                'precio': 99.99,
                'marca': 'Logitech',
                'categoria': 'Accesorios',
                'especificaciones': '''• Sensor: 8000 DPI Darkfield
• Conectividad: Bluetooth, USB Receptor Logi Bolt
• Batería: hasta 70 días con carga completa
• Carga rápida: 3 horas en 1 minuto
• Rueda desplazamiento: MagSpeed electromagnética
• Botones programables: 7
• Compatible: Windows, macOS, Linux, iPadOS
• Flow: control múltiples computadoras
• Construcción: Aluminio y plástico reciclado
• Peso: 141g''',
                'stock': 25
            },
            {
                'nombre': 'Keychron K8 Pro Mechanical',
                'descripcion': 'Teclado mecánico inalámbrico con switches intercambiables hot-swap. RGB personalizable y conexión Bluetooth/Cable. Perfecto para programadores y escritores.',
                'precio': 129.99,
                'marca': 'Keychron',
                'categoria': 'Accesorios',
                'especificaciones': '''• Layout: TKL (87 teclas) - Sin teclado numérico
• Switches: Gateron G Pro Hot-swappable
• Keycaps: PBT Double-shot
• RGB: Por tecla personalizable (QMK/VIA)
• Conectividad: Bluetooth 5.1, USB-C
• Batería: 4000mAh (hasta 240 horas)
• Frame: Aluminio CNC
• Compatible: Windows, macOS, Linux
• Software: QMK/VIA programable
• Peso: 770g''',
                'stock': 18
            },
            {
                'nombre': 'HyperX Cloud II Wireless',
                'descripcion': 'Auriculares gaming inalámbricos con sonido 7.1 surround. Batería de 30 horas, micrófono con cancelación de ruido. Comodidad premium para sesiones largas.',
                'precio': 149.99,
                'marca': 'HyperX',
                'categoria': 'Accesorios',
                'especificaciones': '''• Audio: 7.1 Surround Virtual (PC)
• Drivers: 53mm dinámicos
• Conectividad: Inalámbrica 2.4GHz USB-A
• Batería: hasta 30 horas
• Micrófono: Desmontable con cancelación de ruido
• Controles en auricular: Volumen, silenciar
• Almohadillas: Espuma viscoelástica
• Construcción: Acero y aluminio
• Peso: 309g
• Compatible: PC, PS5, PS4''',
                'stock': 22
            },
            {
                'nombre': 'Logitech C920 HD Pro Webcam',
                'descripcion': 'Cámara web Full HD 1080p ideal para videollamadas, streaming y trabajo remoto. Enfoque automático y corrección de luz avanzada.',
                'precio': 79.99,
                'marca': 'Logitech',
                'categoria': 'Accesorios',
                'especificaciones': '''• Resolución: Full HD 1080p a 30fps / 720p a 60fps
• Lente: vidrio de 5 elementos
• Enfoque automático: Full HD
• Micrófonos: Estéreo duales integrados
• Campo de visión: 78 grados
• Clip universal ajustable
• Corrección de luz HD automática
• Compatible: Windows, macOS, ChromeOS
• USB-A 2.0
• Dimensiones: 94 x 29 x 71 mm''',
                'stock': 30
            },
            {
                'nombre': 'SanDisk Extreme Pro 1TB SSD Portátil',
                'descripcion': 'Disco duro SSD externo de alta velocidad. Perfecto para edición de video, backups rápidos y transferencia de archivos grandes. Resistente a caídas y agua.',
                'precio': 169.99,
                'marca': 'SanDisk',
                'categoria': 'Accesorios',
                'especificaciones': '''• Capacidad: 1TB
• Velocidad lectura: hasta 1050 MB/s
• Velocidad escritura: hasta 1000 MB/s
• Interfaz: USB-C 3.2 Gen 2
• Cable incluido: USB-C a USB-C y adaptador USB-A
• Resistencia: IP55 (polvo y agua)
• Protección caídas: hasta 2 metros
• Cifrado por hardware AES de 256 bits
• Compatible: Windows, macOS, Android
• Dimensiones: 110 x 57 x 10 mm
• Peso: 77g''',
                'stock': 15
            },
            {
                'nombre': 'TP-Link Archer AX73 Router WiFi 6',
                'descripcion': 'Router de alta velocidad con tecnología WiFi 6. Cobertura amplia para hogares grandes, tecnología OFDMA y MU-MIMO para múltiples dispositivos simultáneos.',
                'precio': 129.99,
                'marca': 'TP-Link',
                'categoria': 'Accesorios',
                'especificaciones': '''• Estándar: WiFi 6 (802.11ax)
• Velocidad: hasta 5400 Mbps (5GHz: 4804 Mbps + 2.4GHz: 574 Mbps)
• CPU: Quad-Core 1.5GHz
• Puertos: 1x Gigabit WAN, 4x Gigabit LAN, USB 3.0
• Antenas: 6x externas de alto rendimiento
• Tecnologías: OFDMA, MU-MIMO, Beamforming
• Seguridad: WPA3, HomeShield
• App: TP-Link Tether para gestión
• Cobertura: hasta 250 m²
• Dimensiones: 272.5 x 147.2 x 49.2 mm''',
                'stock': 14
            },
        ]
