# Registro de Cambios - Implementación e-commerce (Computadores) — Consolidado

Fecha: 2025-10-25

Este documento consolida los cambios realizados para transformar el proyecto base en una MVP de e-commerce orientada a la venta de computadores. Incluye detalles de modelos, vistas, plantillas, configuración y pasos para ejecutar y verificar localmente.

## Resumen de alto nivel
- Añadidos campos y funcionalidad de e-commerce a `Producto`.
- Nuevos modelos para gestionar pedidos: `Order` y `OrderItem`.
- Implementado un carrito simple basado en sesión (add/view/checkout).
- Plantillas nuevas: `index.html` (landing marketplace), `producto_detalle.html`, `carrito.html`, `checkout.html`, `orders.html`.
- Configuración de `MEDIA` para imágenes de productos y soportes en views/forms para subida de archivos.

---

## Modelos
- `Producto` (extensión): campos nuevos
	- `marca` (CharField)
	- `categoria` (CharField)
	- `especificaciones` (TextField)
	- `stock` (PositiveIntegerField, default=0)
	- `imagen` (ImageField, upload_to='productos/', null=True, blank=True)
- `Order`:
	- FK a `User`, `total` (DecimalField), `estado` (choices), `creado_el` (DateTimeField)
- `OrderItem`:
	- FK a `Order` y `Producto`, `cantidad`, `precio_unitario` (snapshot del precio al crear la orden)

Notas:
- Se añadieron valores por defecto en campos nuevos de `Producto` para evitar prompts interactivos al ejecutar `makemigrations` sobre una base con datos existentes.

## Admin
- Registradas las nuevas entidades en el admin: `Producto`, `Order`, `OrderItem`.
- Configuración básica de `list_display`, `search_fields` y `list_filter` para facilitar gestión desde el admin.

## Configuración (settings)
- `MEDIA_URL` y `MEDIA_ROOT` añadidos en `settings.py` para servir imágenes subidas en desarrollo.
- En `crud_app/urls.py` y/o `Mi_proyecto_UCC/urls.py` se añadió `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` para servir media en DEBUG.

## Formularios
- `ProductoForm` (ModelForm): actualizado para incluir los nuevos campos y `imagen`.
- `CheckoutForm`: formulario simple para `direccion` y `telefono` usado en el flujo de checkout.

## Vistas implementadas
- `index` — Landing tipo marketplace (muestra una cuadrícula de productos recientes, hasta 12). Incluye la caja de búsqueda (UI) y un botón que lleva a la lista completa de productos.
- `listar_productos` — listado paginado/filtro básico (lista definitiva de productos con imagen, marca y botón "Añadir").
- `producto_detalle` — muestra la ficha completa del producto con imagen, marca, categoría, especificaciones, precio y stock; botón para agregar al carrito.
- `agregar_al_carrito` — añade items al carrito guardado en `request.session` (mapping product_id -> cantidad).
- `ver_carrito` — muestra el contenido del carrito con subtotales y total.
- `checkout` — valida stock, crea `Order` y `OrderItem` (con snapshot de precio), resta stock cuando procede, y limpia el carrito.
- `orders` — lista las órdenes del usuario autenticado.

Errores y correcciones notables durante implementación:
- Evitar mostrar mensajes de error en GET para `crear_producto` / `actualizar_producto` (mensajes solo en POST con validación fallida).
- Importar `Order` y `OrderItem` en `views.py` para evitar NameError.
- Corregir plantillas con sintaxis Django correcta (ej.: `${{ item.precio_unitario }}` en `orders.html`).

## URLs y routing
- Nuevas rutas (en `crud_app/urls.py`):
	- `''` -> `index` (root ahora muestra `index.html`).
	- `productos/` -> `listar_productos`
	- `producto/<int:pk>/` -> `producto_detalle`
	- `carrito/agregar/<int:pk>/` -> `agregar_al_carrito`
	- `carrito/` -> `ver_carrito`
	- `checkout/` -> `checkout`
	- `orders/` -> `orders`

Cambios de navegación:
- `base.html` actualizado para mostrar en la barra de navegación:
	- Enlace visible "Lista de productos" que apunta a `listar_productos`.
	- Icono/enlace "🛒 Ver carrito" apuntando a `ver_carrito`.
	- Enlace a "Mis órdenes" cuando el usuario está autenticado.

## Plantillas
- `index.html` (nuevo):
	- Landing con un header/hero, cuadro de búsqueda (UI sin lógica de backend por defecto), y una cuadrícula de productos recientes (imagen, nombre, precio, enlace a detalle).
	- Botón/link destacado que abre `lista_productos.html` para ver todo el catálogo.
- `lista_productos.html` (modificado): muestra tarjetas con `imagen`, `marca`, `precio`, `stock` y botón "Añadir" (envía a la vista `agregar_al_carrito`).
- `producto_detalle.html` (nuevo): ficha del producto con campos extendidos.
- `crear_producto.html` (modificado): form con `enctype="multipart/form-data"` para permitir subida de `imagen`.
- `carrito.html` (nuevo): tabla con productos del carrito, cantidad editable o botones para ajustar, subtotal y total.
- `checkout.html` (nuevo): formulario de checkout (`CheckoutForm`) para recoger dirección y teléfono.
- `orders.html` (nuevo): listado de órdenes hechas por el usuario con estado y total.

## Media / Imágenes
- Requiere instalar `Pillow` en el entorno para que `ImageField` funcione.
- Asegurarse de ejecutar migraciones y usar `python manage.py runserver` con DEBUG=True para servir media en desarrollo.


## Estado actual y pendientes
- Completado: modelos, admin, media config, producto detalle, lista con imágenes, carrito sesión, checkout y órdenes, landing `index.html` y routing.
- Pendiente / Recomendado:
	- Hacer funcional la búsqueda del `index` (actualmente UI-only).
	- Añadir tests automáticos (models + flujo de compra).
	- Mejorar la UX del carrito (actualizar cantidades en línea, eliminación AJAX).
	- Paginación y filtros por marca/categoría/precio.
	- Crear `requirements.txt` con versiones exactas (si quieres, lo genero ahora).


