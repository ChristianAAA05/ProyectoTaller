"""
Configuración de URLs para la aplicación Taller Mecánico

Este archivo define todas las rutas URL de la aplicación, incluyendo:

- URLs de autenticación (login, logout, perfil)
- URLs de API REST para operaciones CRUD automáticas
- URLs para vistas basadas en plantillas (formularios manuales)
- URLs para ViewSets con routers automáticos

Cada URL tiene un nombre único (name) que se usa en templates y redirecciones.
"""

from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# ========== CONFIGURACIÓN DEL ROUTER ==========
# Router automático para ViewSets que genera URLs REST estándar
router = DefaultRouter()
router.register(r'agendas', views.AgendaViewSet)      # URLs para citas: /agendas/, /agendas/{id}/
router.register(r'registros', views.RegistroViewSet)  # URLs para registros: /registros/, /registros/{id}/

# ========== PATRÓN DE URLS ==========
# Las URLs siguen el patrón estándar de Django:
# path('ruta/', vista, name='nombre_unico')
# path('ruta/<tipo:parametro>/', vista, name='nombre_unico')

urlpatterns = [
    # ========== URLS DE AUTENTICACIÓN ==========
    # Sistema de login/logout y gestión de usuarios
    path('login/', views.login_view, name='login'),           # Página de inicio de sesión
    path('logout/', views.logout_view, name='logout'),        # Cierre de sesión
    path('perfil/', views.perfil_view, name='perfil'),         # Perfil de usuario

    # ========== URLS DE API REST ==========
    # URLs automáticas para operaciones CRUD usando Django REST Framework
    # Estas URLs siguen el patrón REST: GET, POST, PUT, DELETE

    # Clientes - operaciones CRUD automáticas
    path('clientes/', views.ClienteListCreate.as_view(), name='clientes-list-create'),        # GET (listar), POST (crear)
    path('clientes/<int:pk>/', views.ClienteRetrieveUpdateDestroy.as_view(), name='cliente-detail'),  # GET, PUT, DELETE por ID

    # Empleados - operaciones CRUD automáticas
    path('empleados/', views.EmpleadoListCreate.as_view(), name='empleados-list-create'),      # GET (listar), POST (crear)
    path('empleados/<int:pk>/', views.EmpleadoRetrieveUpdateDestroy.as_view(), name='empleado-detail'),  # GET, PUT, DELETE por ID

    # Servicios - operaciones CRUD automáticas
    path('servicios/', views.ServicioListCreate.as_view(), name='servicios-list-create'),      # GET (listar), POST (crear)
    path('servicios/<int:pk>/', views.ServicioRetrieveUpdateDestroy.as_view(), name='servicio-detail'),  # GET, PUT, DELETE por ID

    # Vehículos - operaciones CRUD automáticas
    path('vehiculos/', views.VehiculoListCreate.as_view(), name='vehiculos-list-create'),      # GET (listar), POST (crear)
    path('vehiculos/<int:pk>/', views.VehiculoRetrieveUpdateDestroy.as_view(), name='vehiculo-detail'),  # GET, PUT, DELETE por ID

    # Reparaciones - operaciones CRUD automáticas
    path('reparaciones/', views.ReparacionListCreate.as_view(), name='reparaciones-list-create'),      # GET (listar), POST (crear)
    path('reparaciones/<int:pk>/', views.ReparacionRetrieveUpdateDestroy.as_view(), name='reparacion-detail'),  # GET, PUT, DELETE por ID

    # ========== URLS DE VISTAS BASADAS EN PLANTILLAS ==========
    # Estas son las vistas que renderizan templates HTML para formularios manuales

    # Dashboard principal
    path('inicio/', views.inicio, name='inicio'),  # Página de inicio/dashboard

    # ========== GESTIÓN DE CLIENTES ==========
    path('clientes/lista/', views.clientes_lista, name='clientes-lista'),          # Listar todos los clientes
    path('clientes/crear/', views.clientes_crear, name='clientes-crear'),           # Formulario para crear cliente
    path('clientes/editar/<int:pk>/', views.clientes_editar, name='clientes-editar'),  # Formulario para editar cliente
    path('clientes/eliminar/<int:pk>/', views.clientes_eliminar, name='clientes-eliminar'),  # Confirmación para eliminar cliente

    # ========== GESTIÓN DE EMPLEADOS ==========
    path('empleados/lista/', views.empleados_lista, name='empleados-lista'),          # Listar todos los empleados
    path('empleados/crear/', views.empleados_crear, name='empleados-crear'),           # Formulario para crear empleado
    path('empleados/editar/<int:pk>/', views.empleados_editar, name='empleados-editar'),  # Formulario para editar empleado
    path('empleados/eliminar/<int:pk>/', views.empleados_eliminar, name='empleados-eliminar'),  # Confirmación para eliminar empleado

    # ========== GESTIÓN DE SERVICIOS ==========
    path('servicios/lista/', views.servicios_lista, name='servicios-lista'),          # Listar todos los servicios
    path('servicios/crear/', views.servicios_crear, name='servicios-crear'),           # Formulario para crear servicio
    path('servicios/editar/<int:pk>/', views.servicios_editar, name='servicios-editar'),  # Formulario para editar servicio
    path('servicios/eliminar/<int:pk>/', views.servicios_eliminar, name='servicios-eliminar'),  # Confirmación para eliminar servicio

    # ========== INCLUSIÓN DE ROUTERS ==========
    # Incluye automáticamente las URLs generadas por el router para ViewSets
    # Esto crea URLs como: /agendas/, /agendas/{id}/, /registros/, /registros/{id}/
    path('', include(router.urls)),
]
