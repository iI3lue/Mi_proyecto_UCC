# 🛒 Mi Tienda - E-commerce Django

Sistema de comercio electrónico desarrollado en Django con gestión de productos, categorías, carrito de compras y procesamiento de órdenes.

## 📋 Características

- ✅ Catálogo de productos con imágenes
- ✅ Sistema de categorías
- ✅ Carrito de compras
- ✅ Procesamiento de órdenes
- ✅ Búsqueda de productos
- ✅ Panel de administración
- ✅ Autenticación de usuarios
- ✅ Precios en pesos colombianos (COP)

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### 1. Clonar el Repositorio

```bash
git clone https://github.com/TU-USUARIO/Mi_proyecto_UCC.git
cd Mi_proyecto_UCC
```

### 2. Crear Entorno Virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

**Opción A - Instalación completa (recomendada):**
```bash
pip install -r requirements.txt
```

**Opción B - Instalación mínima:**
```bash
pip install -r requirements-minimal.txt
```

### 4. Configurar la Base de Datos

El proyecto ya incluye una base de datos con datos de prueba (`db.sqlite3`). Si deseas empezar desde cero:

```bash
# Eliminar la base de datos actual
rm db.sqlite3  # Linux/Mac
del db.sqlite3  # Windows

# Crear nueva base de datos
python manage.py migrate
python manage.py createsuperuser
```

### 5. Ejecutar el Servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: **http://127.0.0.1:8000/**

## 👤 Credenciales de Acceso

Si usas la base de datos incluida, puedes acceder con:

- **Usuario:** `juanito`
- **Contraseña:** `123456`
- **Permisos:** Administrador (superuser)

### Acceso al Panel de Administración

Visita: **http://127.0.0.1:8000/admin/**

## 📁 Estructura del Proyecto

```
Mi_proyecto_UCC/
├── crud_app/                    # Aplicación principal
│   ├── migrations/              # Migraciones de base de datos
│   ├── templates/               # Plantillas HTML
│   │   └── crud_app/
│   ├── templatetags/            # Filtros personalizados
│   │   └── custom_filters.py   # Filtro currency_cop
│   ├── static/                  # Archivos estáticos (CSS, JS)
│   ├── models.py                # Modelos de datos
│   ├── views.py                 # Vistas/Controladores
│   ├── urls.py                  # Rutas de la app
│   └── forms.py                 # Formularios
├── Mi_proyecto_UCC/             # Configuración del proyecto
│   ├── settings.py              # Configuración Django
│   └── urls.py                  # Rutas principales
├── media/                       # Archivos subidos (imágenes)
│   └── productos/
├── static/                      # Archivos estáticos del proyecto
├── db.sqlite3                   # Base de datos SQLite
├── manage.py                    # Script de gestión Django
├── requirements.txt             # Dependencias completas
├── requirements-minimal.txt     # Dependencias mínimas
└── README.md                    # Este archivo
```

## 🔧 Configuración Adicional

### Variables de Entorno (Opcional)

Para producción, considera crear un archivo `.env`:

```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=tudominio.com
```

### Archivos Estáticos (Producción)

```bash
python manage.py collectstatic
```

## 📦 Modelos Principales

- **Producto**: Gestión de productos con nombre, precio, descripción, imagen
- **Categoria**: Categorización de productos
- **Carrito**: Carrito de compras temporal
- **ItemCarrito**: Items dentro del carrito
- **Order**: Órdenes de compra
- **OrderItem**: Items de las órdenes

## 🎨 Características del Frontend

- Bootstrap 5.3
- Bootstrap Icons
- Diseño responsivo
- Tema moderno con gradientes
- Formato de moneda colombiana ($4.200.000)

## 📝 Uso del Sistema

### Como Cliente:

1. Navega por los productos
2. Busca productos por nombre/descripción
3. Filtra por categorías
4. Añade productos al carrito
5. Procesa tu orden con información de envío

### Como Administrador:

1. Accede al panel admin: `/admin/`
2. Gestiona productos (crear, editar, eliminar)
3. Gestiona categorías
4. Revisa órdenes de clientes
5. Gestiona usuarios

## 🛠️ Tecnologías Utilizadas

- **Backend:** Django 5.2.7
- **Base de Datos:** SQLite3
- **Frontend:** Bootstrap 5.3, HTML5, CSS3, JavaScript
- **Imágenes:** Pillow 11.3.0
- **Iconos:** Bootstrap Icons

## 📄 Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

## 🐛 Solución de Problemas

### Error: "No module named 'PIL'"
```bash
pip install Pillow
```

### Error: "ModuleNotFoundError: No module named 'crud_app'"
Asegúrate de estar en el directorio correcto y que el entorno virtual esté activado.

### Las imágenes no se muestran
Verifica que la carpeta `media/` tenga los permisos correctos y que `DEBUG=True` en development.

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en GitHub.

---

**Desarrollado con ❤️ usando Django**
