# Taller Mecánico - Proyecto Django

Este proyecto es una aplicación Django para la gestión de un taller mecánico, con API REST (Django REST Framework) y vistas con plantillas básicas.

## Requisitos
- Python 3.11 (recomendado)
- Opcional según base de datos:
  - SQLite: sin requisitos adicionales (por defecto en Python)
  - MariaDB/MySQL: servicio corriendo y librerías nativas para `mysqlclient`

## Entorno virtual e instalación
```bash
# Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# Actualizar pip
python -m pip install -U pip

# Instalar dependencias mínimas para usar SQLite (sin MySQL/MariaDB)
pip install -r requirements2.txt
```

## Configuración de base de datos
El repositorio trae configurado MySQL/MariaDB en `taller_mecanico/settings.py`.
Para evitar dependencias nativas, puedes optar por una de las siguientes opciones:

### Opción A: Usar SQLite (recomendado para evaluación/desarrollo)
1. Edita `taller_mecanico/settings.py` y reemplaza la sección `DATABASES` por:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
2. Guarda los cambios y continúa con migraciones y servidor.

### Opción B: Usar MariaDB/MySQL
1. Instalar librerías del sistema (ejemplo Debian/Ubuntu):
```bash
sudo apt-get update && sudo apt-get install -y default-libmysqlclient-dev build-essential
```
2. Instalar cliente Python:
```bash
pip install "mysqlclient>=2.2,<3"
```
3. Asegúrate de que `DATABASES` en `taller_mecanico/settings.py` contenga tus credenciales:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'taller_mecanico',
        'USER': 'usuario',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
```

## Migraciones y ejecución
```bash
python manage.py migrate
python manage.py runserver
```
- Accede a la app en http://127.0.0.1:8000/
- Endpoints API bajo el prefijo definido en `taller_mecanico/urls.py` (por defecto `api/`).

## Consideraciones adicionales
- `SECRET_KEY` y credenciales de DB están en `settings.py` para desarrollo. No usar en producción.
- Para producción: configurar variables de entorno, `DEBUG = False` y `ALLOWED_HOSTS`.
- Si usas tests, podrías preferir SQLite para evitar dependencias nativas.

## Estructura relevante
- Proyecto: `taller_mecanico/`
  - Configuración: `taller_mecanico/settings.py`, `taller_mecanico/urls.py`
  - Plantillas: `taller_mecanico/templates/`
- App: `gestion/`
  - Modelos: `gestion/models.py`
  - Serializers: `gestion/serializers.py`
  - Vistas: `gestion/views.py`
  - Rutas: `gestion/urls.py`
  - Migraciones: `gestion/migrations/`

## Permisos y Funcionalidades de Usuarios

El sistema de gestión del taller mecánico define dos tipos de usuarios con permisos específicos para mantener la seguridad y eficiencia operativa.

### 👨‍💼 Jefe
- **Control total sobre la administración general del sistema.**
- **Clientes:** Puede agregar, editar y eliminar clientes.
- **Empleados:** Puede agregar, editar y eliminar empleados.
- **Servicios del taller:** Puede agregar, editar y eliminar servicios.

### 👨‍🔧 Encargado
- **Clientes:** Puede agregar y eliminar clientes. Puede editar los datos de los clientes existentes.
- **Agendar citas:** Puede agendar una cita para un cliente que llega presencialmente, seleccionando los servicios requeridos.
- **Visualización de listas:**
  - Ver la lista de servicios disponibles en el taller.
  - Ver la lista de clientes registrados.
  - Ver la lista de empleados registrados.

Estos permisos aseguran que cada rol tenga acceso adecuado a las funcionalidades necesarias para sus responsabilidades diarias.

