from django.contrib import admin
from .models import Producto
from .models import Order, OrderItem

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'marca', 'categoria', 'precio', 'stock', 'creado_el')
	search_fields = ('nombre', 'marca', 'categoria')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'usuario', 'total', 'estado', 'creado_el')
	search_fields = ('usuario__username',)
	list_filter = ('estado',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('order', 'producto', 'cantidad', 'precio_unitario')
	search_fields = ('producto__nombre',)
    
# Register your models here.
