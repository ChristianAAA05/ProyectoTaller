"""
Configuración del proyecto Taller Mecánico

Este archivo contiene toda la configuración del proyecto Django:

- Configuración de base de datos (SQLite por defecto)
- Aplicaciones instaladas (Django apps + app personalizada)
- Configuración de archivos estáticos y de medios
- Configuración de autenticación y permisos
- Configuración de internacionalización
- Middlewares de seguridad y funcionalidad
- Context processors para templates
- URLs de redirección de login/logout

El proyecto está configurado para:
- Usar SQLite como base de datos (ideal para desarrollo)
- Servir archivos estáticos en modo DEBUG
- Usar autenticación personalizada del taller
- Soporte para archivos de medios (imágenes, documentos)
- Configuración de zona horaria para Argentina
"""

from pathlib import Path

# ========== RUTAS DEL PROYECTO ==========
# Rutas base del proyecto para archivos estáticos, plantillas, etc.
BASE_DIR = Path(__file__).resolve().parent.parent

# ========== CONFIGURACIÓN DE SEGURIDAD ==========
# ADVERTENCIA: Cambiar en producción
SECRET_KEY = 'django-insecure-f9&fan5k%)@2b#0ppj*7z*r@(u!-g9fypwy5^v#9am-=2a4j2='
DEBUG = True  # Cambiar a False en producción
ALLOWED_HOSTS = []  # Configurar hosts permitidos en producción

# ========== APLICACIONES INSTALADAS ==========
# Lista de aplicaciones Django que usa el proyecto
INSTALLED_APPS = [
    # Aplicaciones básicas de Django
    'django.contrib.admin',      # Panel de administración
    'django.contrib.auth',       # Sistema de autenticación
    'django.contrib.contenttypes', # Tipos de contenido
    'django.contrib.sessions',   # Manejo de sesiones
    'django.contrib.messages',   # Sistema de mensajes
    'django.contrib.staticfiles', # Manejo de archivos estáticos
    'django.contrib.humanize',   # Filtros para formateo amigable

    # Aplicación principal del taller
    'gestion',                   # Nuestra app personalizada

    # Django REST Framework para API
    'rest_framework',
]

# ========== MIDDLEWARE ==========
# Capas intermedias que procesan las peticiones HTTP
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',        # Seguridad
    'django.contrib.sessions.middleware.SessionMiddleware', # Sesiones
    'django.middleware.common.CommonMiddleware',            # Headers comunes
    'django.middleware.csrf.CsrfViewMiddleware',           # Protección CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Autenticación
    'django.contrib.messages.middleware.MessageMiddleware',  # Mensajes
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Anti-clickjacking
]

# ========== CONFIGURACIÓN DE URLS ==========
ROOT_URLCONF = 'taller_mecanico.urls'  # Archivo principal de URLs

# ========== CONFIGURACIÓN DE TEMPLATES ==========
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Para templates globales en la raíz del proyecto
            BASE_DIR / 'taller_mecanico' / 'templates'  # Para templates en la app principal
        ],
        'APP_DIRS': True,  # Buscar templates en directorios de apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',    # Request en templates
                'django.contrib.auth.context_processors.auth',   # Info de autenticación
                'django.contrib.messages.context_processors.messages', # Mensajes
                'taller_mecanico.settings.permisos_context',     # Funciones de permisos
            ],
        },
    },
]

# ========== APLICACIÓN WSGI ==========
WSGI_APPLICATION = 'taller_mecanico.wsgi.application'

# ========== CONFIGURACIÓN DE BASE DE DATOS ==========
# Base de datos SQLite (ideal para desarrollo)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Archivo de base de datos
    }
}

# ========== VALIDACIÓN DE CONTRASEÑAS ==========
# Validadores de contraseña para mayor seguridad
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ========== INTERNACIONALIZACIÓN ==========
LANGUAGE_CODE = 'es'  # Idioma español
TIME_ZONE = 'America/Asuncion'  # Zona horaria de Argentina
USE_I18N = True  # Internacionalización habilitada
USE_TZ = True    # Zona horaria habilitada

# ========== ARCHIVOS ESTÁTICOS ==========
# Configuración para archivos CSS, JavaScript, imágenes
STATIC_URL = 'static/'  # URL base para archivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / 'taller_mecanico' / 'static',  # Directorio de archivos estáticos
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directorio para collectstatic

# ========== ARCHIVOS DE MEDIOS ==========
# Configuración para archivos subidos por usuarios (imágenes, documentos)
MEDIA_URL = '/media/'   # URL base para archivos de medios
MEDIA_ROOT = BASE_DIR / 'media'  # Directorio físico para archivos

# ========== CLAVE PRIMARIA POR DEFECTO ==========
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========== FUNCIONES DE CONTEXTO GLOBAL ==========
def permisos_context(request):
    """
    Función de contexto global que agrega funciones de permisos a todas las plantillas.

    Permite usar funciones como es_jefe(), puede_gestionar_empleados(), etc.
    directamente en los templates sin necesidad de pasarlas desde las vistas.
    """
    if request.user.is_authenticated:
        from gestion.views import es_jefe, es_encargado, puede_gestionar_empleados, puede_gestionar_servicios

        return {
            'es_jefe': es_jefe(request.user),
            'es_encargado': es_encargado(request.user),
            'puede_gestionar_empleados': puede_gestionar_empleados(request.user),
            'puede_gestionar_servicios': puede_gestionar_servicios(request.user),
        }
    return {}

# ========== CONFIGURACIÓN DE AUTENTICACIÓN ==========
LOGIN_URL = 'login'           # URL de login
LOGIN_REDIRECT_URL = 'inicio' # Redirección después de login exitoso
LOGOUT_REDIRECT_URL = 'login'  # Redirección después de logout

# Backend de autenticación (usando el estándar de Django)
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
