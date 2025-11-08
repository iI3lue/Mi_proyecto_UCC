from django.contrib import admin
from .models import Producto, Categoria, Order, OrderItem

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('icono', 'nombre', 'orden', 'activa', 'get_productos_count', 'actualizado_el')
    list_editable = ('orden', 'activa')
    search_fields = ('nombre', 'descripcion')
    prepopulated_fields = {'slug': ('nombre',)}
    list_filter = ('activa',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'get_categoria_display', 'precio', 'stock', 'creado_el')
    search_fields = ('nombre', 'marca', 'categoria_texto')
    list_filter = ('categoria_fk', 'marca')
    
    def get_categoria_display(self, obj):
        return obj.categoria
    get_categoria_display.short_description = 'Categoría'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'total', 'estado', 'creado_el')
    search_fields = ('usuario__username',)
    list_filter = ('estado',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'producto', 'cantidad', 'precio_unitario')
    search_fields = ('producto__nombre',)
