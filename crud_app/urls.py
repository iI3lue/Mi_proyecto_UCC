#crud_app /forms.py
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('registrarse/', views.register_user, name='register'),
    path('productos', views.listar_productos, name='lista_productos'),
    path('buscar/', views.buscar_productos, name='buscar_productos'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('actualizar/<int:pk>/', views.actualizar_producto, name='actualizar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('producto/<int:pk>/', views.producto_detalle, name='producto_detalle'),
    path('carrito/agregar/<int:pk>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    # Categorías
    path('categorias/', views.categorias_lista, name='categorias_lista'),
    path('categoria/<slug:slug>/', views.categoria_detalle, name='categoria_detalle'),
    # API Endpoints
    path('api/cart/count/', views.cart_count, name='cart_count'),
    path('api/cart/update/', views.cart_update, name='cart_update'),
    path('api/cart/remove/', views.cart_remove, name='cart_remove'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


