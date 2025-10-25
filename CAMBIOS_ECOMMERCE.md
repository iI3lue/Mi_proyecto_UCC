# Registro de Cambios - Implementación e-commerce Django

## Modelos
- Extensión del modelo `Producto`:
  - Nuevos campos: `marca`, `categoria`, `especificaciones`, `stock`, `imagen`.
- Creación de modelos:
  - `Order`: usuario, total, estado, fecha.
  - `OrderItem`: relación con `Order` y `Producto`, cantidad, precio unitario.

## Admin
- Registro de `Producto`, `Order` y `OrderItem` en el panel admin con columnas útiles y búsqueda.

## Configuración
- Agregado en `settings.py`:
  - `MEDIA_URL` y `MEDIA_ROOT` para servir imágenes subidas.
- Instrucción para servir archivos media en desarrollo en `urls.py`.

## Formularios
- Extensión de `ProductoForm` para incluir todos los campos relevantes y el campo de imagen.

## Vistas
- Vista de detalle de producto (`producto_detalle`).
- Vistas de carrito:
  - `agregar_al_carrito`: añade productos al carrito usando la sesión.
  - `ver_carrito`: muestra el contenido del carrito y el total.
- Modificación de `crear_producto` para aceptar imágenes (`request.FILES`).

## URLs
- Nuevas rutas en `crud_app/urls.py`:
  - `/producto/<int:pk>/` para detalle de producto.
  - `/carrito/agregar/<int:pk>/` para añadir al carrito.
  - `/carrito/` para ver el carrito.

## Plantillas
- `lista_productos.html`: muestra imagen, marca, stock, enlaces al detalle y botón "Ver".
- `producto_detalle.html`: muestra todos los datos del producto y botón para agregar al carrito.
- `carrito.html`: muestra productos en el carrito, imagen, cantidad, subtotal y total.
- `crear_producto.html`: permite subir imagen (formulario con `enctype="multipart/form-data"`).
- `base.html`: botón "🛒 Ver carrito" en la barra de navegación.

## Otros
- Migraciones aplicadas para los nuevos campos y modelos.
- Instrucciones para ejecutar y probar el sistema.

---


Este documento resume todos los cambios realizados para transformar el proyecto en una base funcional de e-commerce para venta de computadores.
