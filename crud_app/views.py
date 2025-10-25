from .forms import CheckoutForm
# --- Checkout ---
from django.contrib.auth.decorators import login_required

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
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Order, OrderItem
from .forms import ProductoForm
from django.contrib import messages #para mensajes de alerta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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
        form = ProductoForm(request.POST, instance=producto)
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
    return render(request, 'crud_app/index.html', {'productos': productos})

