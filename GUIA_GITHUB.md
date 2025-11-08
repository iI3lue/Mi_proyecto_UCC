# 📤 Guía para Subir el Proyecto a GitHub

## Paso 1: Preparar el Repositorio Local

```bash
# Verificar el estado de los archivos
git status

# Agregar el README
git add README.md

# Commit del README
git commit -m "docs: agregar README con instrucciones de instalación"

# Verificar que todo esté limpio
git status
```

## Paso 2: Crear Repositorio en GitHub

1. Ve a https://github.com
2. Haz clic en el botón **"New"** (repositorio nuevo)
3. Nombre del repositorio: `Mi_proyecto_UCC` o el que prefieras
4. Descripción: "E-commerce desarrollado en Django"
5. Selecciona **Public** o **Private**
6. **NO** marques "Add a README file" (ya lo tenemos)
7. Haz clic en **"Create repository"**

## Paso 3: Conectar y Subir

GitHub te mostrará instrucciones, usa estas:

```bash
# Si ya tienes el repositorio iniciado (ya tienes commits):
git remote add origin https://github.com/TU-USUARIO/Mi_proyecto_UCC.git
git branch -M main
git push -u origin main
```

**O si prefieres SSH:**

```bash
git remote add origin git@github.com:TU-USUARIO/Mi_proyecto_UCC.git
git branch -M main
git push -u origin main
```

## Paso 4: Verificar

Recarga la página de tu repositorio en GitHub y deberías ver todos los archivos.

---

# 📥 Guía para que Otros Descarguen y Ejecuten

## Método 1: Clonar con Git (Recomendado)

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU-USUARIO/Mi_proyecto_UCC.git

# 2. Entrar al directorio
cd Mi_proyecto_UCC

# 3. Crear entorno virtual
python -m venv venv

# 4. Activar entorno virtual
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Ejecutar el servidor
python manage.py runserver
```

## Método 2: Descargar ZIP

1. En GitHub, haz clic en el botón verde **"Code"**
2. Selecciona **"Download ZIP"**
3. Descomprime el archivo
4. Sigue los pasos 2-6 del Método 1

---

# ⚠️ Notas Importantes

## Archivos Incluidos

El proyecto incluye:
- ✅ `db.sqlite3` - Base de datos con productos y usuario de prueba
- ✅ `media/productos/` - Imágenes de productos
- ✅ Configuración completa de Django

## Usuario de Prueba

- Usuario: `juanito`
- Contraseña: `123456`
- Es superusuario (acceso admin)

## Si Quieres Empezar desde Cero

```bash
# Eliminar base de datos
rm db.sqlite3  # Linux/Mac
del db.sqlite3  # Windows

# Crear nueva base de datos
python manage.py migrate

# Crear tu propio superusuario
python manage.py createsuperuser
```

---

# 🔐 Seguridad para Producción

Si vas a deployar en producción:

1. **Cambia el SECRET_KEY** en `settings.py`
2. **Configura DEBUG=False**
3. **Configura ALLOWED_HOSTS**
4. **Usa variables de entorno** para datos sensibles
5. **Cambia las contraseñas** de los usuarios
6. **Usa PostgreSQL** en lugar de SQLite

Ejemplo de variables de entorno:

```python
# settings.py
import os
from pathlib import Path

SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-por-defecto-para-desarrollo')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

---

# 📝 Comandos Útiles de Git

```bash
# Ver estado
git status

# Agregar cambios
git add .

# Hacer commit
git commit -m "descripción de cambios"

# Subir cambios
git push

# Ver historial
git log --oneline

# Crear nueva rama
git checkout -b nombre-rama

# Cambiar de rama
git checkout main
```

---

# 🆘 Problemas Comunes

## Error: "Permission denied (publickey)"

Necesitas configurar SSH keys. Usa HTTPS en su lugar:
```bash
git remote set-url origin https://github.com/TU-USUARIO/Mi_proyecto_UCC.git
```

## Error: "fatal: remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/TU-USUARIO/Mi_proyecto_UCC.git
```

## El push pide usuario y contraseña todo el tiempo

Usa un token de acceso personal (PAT):
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Marca scope: `repo`
4. Usa el token como contraseña

---

**¡Listo! Tu proyecto está en GitHub y otros pueden descargarlo y ejecutarlo fácilmente** 🎉
