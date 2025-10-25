#crud_app/views.py
from django.shortcuts import render, redirect, get_object_or_404, redirect
from .models import Producto
from .forms import ProductoForm
from django.contrib import messages #para mensajes de alerta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Visitar para listar todos los productos
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'crud_app/lista_productos.html', {'productos': productos})

# Visitar para crear un nuevo producto
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('lista_productos')
    else:
        messages.error(request, 'Error al crear el producto. Por favor, revisar los datos.')
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
        messages.error(request, 'Error al actualizar el producto. Por favor, revisar los datos.')
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

