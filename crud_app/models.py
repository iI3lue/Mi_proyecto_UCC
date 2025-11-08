from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

class Categoria(models.Model):
    """Modelo para categorías de productos"""
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    descripcion = models.TextField(blank=True, help_text="Descripción de la categoría")
    icono = models.CharField(max_length=50, default="📦", help_text="Emoji o código del icono")
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)
    activa = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0, help_text="Orden de visualización")
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.icono} {self.nombre}"

    def get_productos_count(self):
        """Retorna el número de productos en esta categoría"""
        return self.productos.filter(stock__gt=0).count()

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.CharField(max_length=50, default="Sin marca")
    # Mantener compatibilidad con CharField pero agregar ForeignKey
    categoria_texto = models.CharField(max_length=50, default="General", verbose_name="Categoría (texto)")
    categoria_fk = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='productos',
        verbose_name="Categoría"
    )
    especificaciones = models.TextField(blank=True, help_text="Detalles técnicos, formato libre")
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    creado_el = models.DateTimeField(auto_now_add=True)

    @property
    def categoria(self):
        """Propiedad para mantener compatibilidad - retorna nombre de categoría"""
        if self.categoria_fk:
            return self.categoria_fk.nombre
        return self.categoria_texto

    def __str__(self):
        return f"{self.nombre} ({self.marca})"

class Order(models.Model):
    STATUS_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    )
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    creado_el = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')

    def __str__(self):
        return f"Orden #{self.id} - {self.usuario.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Orden #{self.order.id})"
