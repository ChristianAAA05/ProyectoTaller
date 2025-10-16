"""
Decoradores de permisos para la aplicación Taller Mecánico

Este archivo define decoradores personalizados que controlan el acceso
a diferentes funcionalidades según el rol del usuario:

- jefe_required: Solo permite acceso al jefe del taller
- empleados_management_required: Controla acceso a gestión de empleados
- servicios_management_required: Controla acceso a gestión de servicios

Los decoradores verifican automáticamente si el usuario está autenticado
y tiene los permisos necesarios, redirigiendo con mensajes de error si no.
"""

from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

# ========== FUNCIONES DE VERIFICACIÓN DE PERMISOS ==========

def es_jefe(user):
    """
    Verifica si el usuario es jefe del taller.

    Un usuario es considerado jefe si:
    - No tiene perfil de empleado (es administrador)
    - O tiene perfil de empleado con puesto 'jefe'

    Returns:
        bool: True si es jefe, False en caso contrario
    """
    try:
        # Si no es empleado o es jefe, tiene permisos completos
        return not user.profile.es_empleado or user.profile.empleado_relacionado.puesto.lower() == 'jefe'
    except:
        # Si hay error al acceder al perfil, no tiene permisos
        return False

def es_encargado(user):
    """
    Verifica si el usuario es un encargado con permisos limitados.

    Un usuario es considerado encargado si:
    - Tiene perfil de empleado
    - Su puesto es 'encargado' o 'supervisor'

    Returns:
        bool: True si es encargado, False en caso contrario
    """
    try:
        return (user.profile.es_empleado and
                user.profile.empleado_relacionado.puesto.lower() in ['encargado', 'supervisor'])
    except:
        return False

def puede_gestionar_empleados(user):
    """
    Verifica si el usuario puede gestionar empleados.

    Solo el jefe puede gestionar empleados (crear, editar, eliminar).

    Returns:
        bool: True si puede gestionar empleados, False en caso contrario
    """
    return es_jefe(user)

def puede_gestionar_servicios(user):
    """
    Verifica si el usuario puede gestionar servicios.

    Solo el jefe puede gestionar el catálogo de servicios.

    Returns:
        bool: True si puede gestionar servicios, False en caso contrario
    """
    return es_jefe(user)

# ========== DECORADORES DE CONTROL DE ACCESO ==========

def jefe_required(view_func):
    """
    Decorador que requiere que el usuario sea jefe del taller.

    Verifica que el usuario esté autenticado y sea jefe.
    Si no cumple los requisitos, redirige con mensaje de error.

    Uso:
        @jefe_required
        def mi_vista(request):
            # Solo accesible por el jefe
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificación 1: Usuario debe estar autenticado
        if not request.user.is_authenticated:
            return redirect('login')

        # Verificación 2: Usuario debe ser jefe
        if not es_jefe(request.user):
            messages.error(request, 'No tienes permisos para acceder a esta función.')
            return redirect('inicio')

        # Si pasa las verificaciones, ejecutar la función original
        return view_func(request, *args, **kwargs)
    return wrapper

def empleados_management_required(view_func):
    """
    Decorador que requiere permisos para gestionar empleados.

    Controla el acceso a funciones de crear, editar y eliminar empleados.
    Solo el jefe puede realizar estas operaciones.

    Uso:
        @empleados_management_required
        def gestionar_empleados(request):
            # Solo el jefe puede acceder
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificación 1: Usuario debe estar autenticado
        if not request.user.is_authenticated:
            return redirect('login')

        # Verificación 2: Usuario debe poder gestionar empleados (ser jefe)
        if not puede_gestionar_empleados(request.user):
            messages.error(request, 'No tienes permisos para gestionar empleados.')
            return redirect('empleados-lista')

        # Si pasa las verificaciones, ejecutar la función original
        return view_func(request, *args, **kwargs)
    return wrapper

def servicios_management_required(view_func):
    """
    Decorador que requiere permisos para gestionar servicios.

    Controla el acceso a funciones de crear, editar y eliminar servicios
    del catálogo. Solo el jefe puede realizar estas operaciones.

    Uso:
        @servicios_management_required
        def gestionar_servicios(request):
            # Solo el jefe puede acceder
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificación 1: Usuario debe estar autenticado
        if not request.user.is_authenticated:
            return redirect('login')

        # Verificación 2: Usuario debe poder gestionar servicios (ser jefe)
        if not puede_gestionar_servicios(request.user):
            messages.error(request, 'No tienes permisos para gestionar servicios.')
            return redirect('servicios-lista')

        # Si pasa las verificaciones, ejecutar la función original
        return view_func(request, *args, **kwargs)
    return wrapper
