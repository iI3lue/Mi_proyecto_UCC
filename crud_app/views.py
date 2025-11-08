from .forms import CheckoutForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Order, OrderItem, Categoria
from .forms import ProductoForm
from django.contrib import messages #para mensajes de alerta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

@login_required(login_url='login')
def checkout(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0
    for pk, cantidad in carrito.items():
        producto = Producto.objects.filter(pk=pk).first()
        if producto:
            subtotal = producto.precio * cantidad
            productos.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
            total += subtotal

    if not productos:
        messages.error(request, 'El carrito está vacío.')
        return redirect('ver_carrito')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Validar stock
            for item in productos:
                if item['cantidad'] > item['producto'].stock:
                    messages.error(request, f"No hay suficiente stock para {item['producto'].nombre}.")
                    return redirect('ver_carrito')
            # Crear orden
            order = Order.objects.create(
                usuario=request.user,
                total=total,
                estado='pendiente'
            )
            for item in productos:
                OrderItem.objects.create(
                    order=order,
                    producto=item['producto'],
                    cantidad=item['cantidad'],
                    precio_unitario=item['producto'].precio
                )
                # Descontar stock
                item['producto'].stock -= item['cantidad']
                item['producto'].save()
            # Limpiar carrito
            request.session['carrito'] = {}
            messages.success(request, '¡Compra realizada con éxito!')
            return redirect('orders')
    else:
        form = CheckoutForm()
    return render(request, 'crud_app/checkout.html', {'productos': productos, 'total': total, 'form': form})
# --- Historial de órdenes ---
@login_required(login_url='login')
def orders(request):
    ordenes = Order.objects.filter(usuario=request.user).order_by('-creado_el')
    return render(request, 'crud_app/orders.html', {'ordenes': ordenes})
# --- Carrito ---
from django.http import HttpResponseRedirect

def agregar_al_carrito(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    carrito = request.session.get('carrito', {})
    carrito[str(pk)] = carrito.get(str(pk), 0) + 1
    request.session['carrito'] = carrito
    
    # Soporte para AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.method == 'POST':
        return JsonResponse({
            'success': True,
            'message': f"{producto.nombre} agregado al carrito.",
            'count': sum(carrito.values())
        })
    
    messages.success(request, f"{producto.nombre} agregado al carrito.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0
    for pk, cantidad in carrito.items():
        producto = Producto.objects.filter(pk=pk).first()
        if producto:
            subtotal = producto.precio * cantidad
            productos.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
            total += subtotal
    return render(request, 'crud_app/carrito.html', {'productos': productos, 'total': total})
#crud_app/views.py


# Visitar para listar todos los productos
def listar_productos(request):
    # Mostrar solo productos con stock disponible
    productos = Producto.objects.filter(stock__gt=0).order_by('-creado_el')
    return render(request, 'crud_app/lista_productos.html', {'productos': productos})

# Visitar para crear un nuevo producto
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('lista_productos')
        else:
            # Mostrar errores de validación al usuario, sin redirigir
            messages.error(request, 'Error al crear el producto. Por favor, revisar los datos.')
    else:
        form = ProductoForm()
    return render(request, 'crud_app/crear_producto.html', {'form': form})

# Visitar para actualizar un producto existente
def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('lista_productos')
        else:
            # Mostrar errores de validación al usuario, sin redirigir
            messages.error(request, 'Error al actualizar el producto. Por favor, revisar los datos.')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'crud_app/actualizar_producto.html', {'form': form})

# Visitar para eliminar un producto
def eliminar_producto(request, pk): 
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('lista_productos')
    return render(request, 'crud_app/eliminar_producto.html', {'producto': producto})   

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {username}')
            # Redirigir a la lista de productos después de iniciar sesión
            return redirect('lista_productos')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('login')
    return render(request, 'crud_app/login.html')

def logout_user(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente')
    return redirect('login')
def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está en uso')
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, 'Cuenta creada con éxito. Ahora puedes iniciar sesión')
        return redirect('login')

    return render(request, 'crud_app/register.html')

# Vista de detalle de producto
def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'crud_app/producto_detalle.html', {'producto': producto})


def index(request):
    # Mostrar algunos productos destacados y caja de búsqueda básica
    productos = Producto.objects.filter(stock__gt=0).order_by('-creado_el')[:12]
    
    # Obtener categorías activas con conteo de productos
    categorias = Categoria.objects.filter(activa=True).order_by('orden', 'nombre')[:7]
    for categoria in categorias:
        categoria.productos_count = categoria.productos.filter(stock__gt=0).count()
    
    return render(request, 'crud_app/index.html', {
        'productos': productos,
        'categorias': categorias
    })

# ============================================
# API ENDPOINTS PARA AJAX
# ============================================

def cart_count(request):
    """Retorna el número de items en el carrito"""
    carrito = request.session.get('carrito', {})
    count = sum(carrito.values())
    return JsonResponse({'count': count})

@require_POST
def cart_update(request):
    """Actualiza la cantidad de un producto en el carrito"""
    import json
    data = json.loads(request.body)
    product_id = str(data.get('product_id'))
    quantity = int(data.get('quantity', 1))
    
    carrito = request.session.get('carrito', {})
    
    if quantity > 0:
        carrito[product_id] = quantity
    else:
        carrito.pop(product_id, None)
    
    request.session['carrito'] = carrito
    
    # Calcular totales
    total = 0
    subtotal = 0
    producto = Producto.objects.filter(pk=product_id).first()
    if producto:
        subtotal = float(producto.precio) * quantity
    
    for pk, cant in carrito.items():
        prod = Producto.objects.filter(pk=pk).first()
        if prod:
            total += float(prod.precio) * cant
    
    return JsonResponse({
        'success': True,
        'quantity': quantity,
        'subtotal': subtotal,
        'total': total
    })

@require_POST
def cart_remove(request):
    """Elimina un producto del carrito"""
    import json
    data = json.loads(request.body)
    product_id = str(data.get('product_id'))
    
    carrito = request.session.get('carrito', {})
    carrito.pop(product_id, None)
    request.session['carrito'] = carrito
    
    # Calcular total
    total = 0
    for pk, cant in carrito.items():
        prod = Producto.objects.filter(pk=pk).first()
        if prod:
            total += float(prod.precio) * cant
    
    return JsonResponse({
        'success': True,
        'total': total
    })

# ============================================
# BÚSQUEDA Y FILTROS
# ============================================

def buscar_productos(request):
    """Vista de búsqueda con filtros"""
    query = request.GET.get('q', '')
    categoria_slug = request.GET.get('category', '')
    precio_orden = request.GET.get('price', '')
    marca = request.GET.get('marca', '')
    
    # Empezar con todos los productos con stock
    productos = Producto.objects.filter(stock__gt=0)
    
    # Aplicar búsqueda por texto
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(marca__icontains=query) |
            Q(categoria_texto__icontains=query) |
            Q(categoria_fk__nombre__icontains=query) |
            Q(especificaciones__icontains=query)
        )
    
    # Filtrar por categoría (usando slug o nombre)
    if categoria_slug:
        productos = productos.filter(
            Q(categoria_fk__slug=categoria_slug) | Q(categoria_texto=categoria_slug)
        )
    
    # Filtrar por marca
    if marca:
        productos = productos.filter(marca=marca)
    
    # Ordenar por precio
    if precio_orden == 'asc':
        productos = productos.order_by('precio')
    elif precio_orden == 'desc':
        productos = productos.order_by('-precio')
    else:
        productos = productos.order_by('-creado_el')
    
    # Obtener categorías y marcas únicas para los filtros
    categorias = Categoria.objects.filter(activa=True).order_by('orden', 'nombre')
    marcas = Producto.objects.values_list('marca', flat=True).distinct().order_by('marca')
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'marcas': marcas,
        'query': query,
        'selected_category': categoria_slug,
        'selected_marca': marca,
        'selected_price': precio_orden,
    }
    
    return render(request, 'crud_app/buscar.html', context)


def categorias_lista(request):
    """Vista que muestra todas las categorías disponibles"""
    categorias = Categoria.objects.filter(activa=True).order_by('orden', 'nombre')
    
    # Contar productos con stock para cada categoría
    for categoria in categorias:
        categoria.productos_count = categoria.productos.filter(stock__gt=0).count()
    
    context = {
        'categorias': categorias,
    }
    
    return render(request, 'crud_app/categorias.html', context)


def categoria_detalle(request, slug):
    """Vista que muestra todos los productos de una categoría específica"""
    categoria = get_object_or_404(Categoria, slug=slug, activa=True)
    
    # Obtener productos con stock de esta categoría
    productos = categoria.productos.filter(stock__gt=0)
    
    # Filtro de precio opcional
    precio_orden = request.GET.get('price', '')
    if precio_orden == 'asc':
        productos = productos.order_by('precio')
    elif precio_orden == 'desc':
        productos = productos.order_by('-precio')
    else:
        productos = productos.order_by('-creado_el')
    
    # Obtener marcas disponibles en esta categoría
    marcas = productos.values_list('marca', flat=True).distinct().order_by('marca')
    
    # Filtro de marca opcional
    marca = request.GET.get('marca', '')
    if marca:
        productos = productos.filter(marca=marca)
    
    context = {
        'categoria': categoria,
        'productos': productos,
        'marcas': marcas,
        'selected_marca': marca,
        'selected_price': precio_orden,
    }
    
    return render(request, 'crud_app/categoria_detalle.html', context)