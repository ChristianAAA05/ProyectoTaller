"""
Configuración de URLs principal para el proyecto Taller Mecánico

Este archivo configura las rutas URL principales del proyecto Django,
incluyendo:

- Redirección automática según estado de autenticación
- Panel de administración de Django
- URLs de la aplicación principal (gestion)
- Configuración de archivos estáticos y de medios
- Sobrescritura de URLs de autenticación estándar

Las URLs están diseñadas para:
- Redirigir usuarios no autenticados al login
- Proporcionar acceso directo al dashboard para usuarios autenticados
- Incluir todas las funcionalidades de la aplicación de gestión
- Servir archivos estáticos en modo desarrollo
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# ========== URLS PRINCIPALES DEL PROYECTO ==========
urlpatterns = [
    # ========== PANEL DE ADMINISTRACIÓN ==========
    # Django admin para gestión avanzada de la base de datos
    path('admin/', admin.site.urls),

    # ========== REDIRECCIÓN INTELIGENTE ==========
    # Redirección condicional según el estado de autenticación del usuario
    # - Si está autenticado: redirige al dashboard (inicio)
    # - Si no está autenticado: redirige al login
    path('', lambda request: redirect('inicio') if request.user.is_authenticated else redirect('login')),

    # ========== APLICACIÓN PRINCIPAL ==========
    # Incluye todas las URLs de la aplicación de gestión del taller
    # Esto incluye autenticación, CRUD de entidades, API REST, etc.
    path('', include('gestion.urls')),
]

# ========== CONFIGURACIÓN PARA ARCHIVOS ESTÁTICOS ==========
# Servir archivos de medios (imágenes, documentos) en modo desarrollo
# Esto es necesario para que los archivos subidos sean accesibles
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ========== CONFIGURACIÓN DE AUTENTICACIÓN ==========
# Sobrescritura de las URLs de autenticación estándar de Django
# para usar nuestras vistas personalizadas de login/logout

from django.urls import path
from gestion.views import login_view

# Insertar URL personalizada de login al inicio de urlpatterns
# Esto sobreescribe la URL de login estándar de Django (/accounts/login/)
# con nuestra vista personalizada que incluye lógica específica del taller
urlpatterns.insert(0, path('accounts/login/', login_view, name='accounts_login'))
