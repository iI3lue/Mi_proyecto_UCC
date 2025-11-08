# 📦 Instalación del Proyecto en Otro Computador

## 📋 Requisitos Previos
- Python 3.9 o superior instalado
- pip (gestor de paquetes de Python)

## 🚀 Pasos de Instalación

### 1️⃣ Descomprimir el Proyecto
Descomprime la carpeta `Mi_proyecto_UCC` en la ubicación deseada.

### 2️⃣ Abrir Terminal
Abre PowerShell o CMD y navega a la carpeta del proyecto:
```powershell
cd ruta/donde/descomprimiste/Mi_proyecto_UCC
```

### 3️⃣ Instalar Dependencias

**Opción A - Instalación Mínima (Recomendada)**:
```powershell
pip install -r requirements-minimal.txt
```

**Opción B - Instalación Completa**:
```powershell
pip install -r requirements.txt
```

### 4️⃣ Iniciar el Servidor
```powershell
python manage.py runserver
```

### 5️⃣ Acceder al Sitio
Abre tu navegador en: **http://127.0.0.1:8000/**

---

## 🔑 Credenciales de Acceso

### Usuario Administrador:
- **Usuario**: `juanito`
- **Contraseña**: `123456`

### URLs Importantes:
- **Inicio**: http://127.0.0.1:8000/
- **Admin Django**: http://127.0.0.1:8000/admin/
- **Productos**: http://127.0.0.1:8000/productos
- **Categorías**: http://127.0.0.1:8000/categorias/
- **Búsqueda**: http://127.0.0.1:8000/buscar/

---

## 📊 Datos Incluidos

El proyecto ya incluye:
- ✅ **7 Categorías** de productos
- ✅ **19 Productos** con especificaciones
- ✅ **2 Usuarios** registrados (juanito y Juan Diego)
- ✅ Sistema de carrito de compras
- ✅ Sistema de órdenes
- ✅ Tema claro/oscuro

---

## 🛠️ Comandos Útiles

### Crear nuevo superusuario:
```powershell
python manage.py createsuperuser
```

### Poblar más productos:
```powershell
python manage.py poblar_productos
```

### Poblar categorías:
```powershell
python manage.py poblar_categorias
```

### Ver productos por categoría:
```powershell
python manage.py shell -c "from crud_app.models import Categoria; [print(f'{cat.icono} {cat.nombre}: {cat.productos.count()} productos') for cat in Categoria.objects.all()]"
```

---

## ⚠️ Solución de Problemas

### Error: "No module named 'django'"
```powershell
pip install django pillow
```

### Error: "Port 8000 is already in use"
Usa otro puerto:
```powershell
python manage.py runserver 8080
```

### El servidor no arranca
Verifica que estés en la carpeta correcta (debe contener `manage.py`):
```powershell
dir
# Debe mostrar manage.py, db.sqlite3, crud_app/, etc.
```

### Olvidé la contraseña
Cambia la contraseña del usuario juanito:
```powershell
python manage.py shell -c "from django.contrib.auth.models import User; u=User.objects.get(username='juanito'); u.set_password('nuevacontraseña123'); u.save(); print('Contraseña cambiada')"
```

---

## 📚 Estructura del Proyecto

```
Mi_proyecto_UCC/
├── db.sqlite3                    # Base de datos (¡NO eliminar!)
├── manage.py                     # Script principal de Django
├── requirements.txt              # Todas las dependencias
├── requirements-minimal.txt      # Solo dependencias esenciales
├── crud_app/                     # Aplicación principal
│   ├── models.py                # Modelos (Producto, Categoria, etc.)
│   ├── views.py                 # Lógica de vistas
│   ├── urls.py                  # Rutas URL
│   ├── templates/               # Plantillas HTML
│   └── management/commands/     # Comandos personalizados
├── static/                       # CSS y JavaScript
│   ├── css/styles.css
│   └── js/main.js
├── media/                        # Imágenes de productos
│   └── productos/
└── Mi_proyecto_UCC/             # Configuración del proyecto
    └── settings.py              # Configuración principal
```

---

## 🎯 Características del Sistema

### 🛒 Funcionalidades de Usuario:
- Ver catálogo de productos
- Buscar productos con filtros
- Agregar al carrito (AJAX)
- Realizar órdenes de compra
- Ver historial de órdenes
- Cambiar tema claro/oscuro

### 👨‍💼 Funcionalidades de Admin:
- Gestionar productos (CRUD completo)
- Gestionar categorías
- Ver todas las órdenes
- Administrar usuarios
- Subir imágenes de productos

### 🎨 Diseño:
- Tema claro/oscuro con localStorage
- Diseño responsive (móvil, tablet, desktop)
- Animaciones suaves
- Color principal: Azul #64b5f6
- Interfaz minimalista y moderna

---

## 💾 Backup de la Base de Datos

Para hacer backup de tus datos:
```powershell
# Simplemente copia el archivo db.sqlite3
copy db.sqlite3 db.sqlite3.backup
```

Para restaurar:
```powershell
copy db.sqlite3.backup db.sqlite3
```

---

## 📞 Soporte

Si tienes problemas, revisa:
1. `GUIA_MIGRACION_CATEGORIAS.md` - Sistema de categorías
2. `COMO_POBLAR_PRODUCTOS.md` - Gestión de productos
3. `MEJORAS_IMPLEMENTADAS.md` - Historial de cambios
4. `SISTEMA_CATEGORIAS_RESUMEN.md` - Resumen completo

---

**¡Disfruta tu ecommerce! 🎉**

*Versión del proyecto: Noviembre 2025*
