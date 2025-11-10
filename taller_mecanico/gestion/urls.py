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

    # ========== URLS DE DASHBOARDS ==========
    # Página de inicio que redirige según el rol del usuario
    path('inicio/', views.inicio, name='inicio'),
    
    # Dashboard para el jefe del taller
    path('dashboard-jefe/', views.dashboard_jefe, name='dashboard_jefe'),
    
    # Dashboard para el encargado
    path('dashboard-encargado/', views.dashboard_encargado, name='dashboard_encargado'),
    
    # Dashboard de reparaciones
    path('reparaciones/', views.dashboard_reparaciones, name='dashboard_reparaciones'),
    path('reparaciones/nueva/', views.crear_reparacion, name='crear_reparacion'),
    path('reparaciones/editar/<int:pk>/', views.editar_reparacion, name='editar_reparacion'),
    path('reparaciones/eliminar/<int:pk>/', views.eliminar_reparacion, name='eliminar_reparacion'),
    # Reportes
    path('reportes/ingresos/', views.reportes_ingresos, name='reportes_ingresos'),
    path('reportes/ingresos/exportar/', views.exportar_ingresos_excel, name='exportar_ingresos_excel'),
    
    # ========== URLS DE API REST ==========
    # URLs automáticas para operaciones CRUD usando Django REST Framework
    # Estas URLs siguen el patrón REST: GET, POST, PUT, DELETE

    # ========== GESTIÓN DE VEHÍCULOS ==========
    # Listado de vehículos
    path('vehiculos/', views.VehiculoListView.as_view(), name='vehiculos-lista'),
    path('vehiculos/agregar/', views.vehiculo_agregar, name='vehiculo-agregar'),
    path('vehiculos/agregar/<int:cliente_id>/', views.vehiculo_agregar, name='vehiculo-agregar-cliente'),
    path('vehiculos/editar/<int:pk>/', views.vehiculo_editar, name='vehiculo-editar'),
    path('vehiculos/eliminar/<int:pk>/', views.vehiculo_eliminar, name='vehiculo-eliminar'),
    path('api/clientes/buscar/', views.buscar_clientes, name='buscar-clientes'),
    
    # Clientes - operaciones CRUD automáticas
    path('clientes/', views.ClienteListCreate.as_view(), name='clientes-list-create'),        # GET (listar), POST (crear)
    path('clientes/<int:pk>/', views.ClienteRetrieveUpdateDestroy.as_view(), name='cliente-detail'),  # GET, PUT, DELETE por ID

    # Empleados - operaciones CRUD automáticas
    path('empleados/', views.EmpleadoListCreate.as_view(), name='empleados-list-create'),      # GET (listar), POST (crear)
    path('empleados/<int:pk>/', views.EmpleadoRetrieveUpdateDestroy.as_view(), name='empleado-detail'),  # GET, PUT, DELETE por ID

    # Servicios - operaciones CRUD automáticas
    path('servicios/', views.ServicioListCreate.as_view(), name='servicios-list-create'),      # GET (listar), POST (crear)
    path('servicios/<int:pk>/', views.ServicioRetrieveUpdateDestroy.as_view(), name='servicio-detail'),  # GET, PUT, DELETE por ID

    # API Vehículos - operaciones CRUD automáticas
    path('api/vehiculos/', views.VehiculoListCreate.as_view(), name='api-vehiculos-list-create'),      # GET (listar), POST (crear)
    path('api/vehiculos/<int:pk>/', views.VehiculoRetrieveUpdateDestroy.as_view(), name='api-vehiculo-detail'),  # GET, PUT, DELETE por ID

    # Reparaciones - operaciones CRUD automáticas (API)
    path('api/reparaciones/', views.ReparacionListCreate.as_view(), name='api-reparaciones-list-create'),      # GET (listar), POST (crear)
    path('api/reparaciones/<int:pk>/', views.ReparacionRetrieveUpdateDestroy.as_view(), name='api-reparacion-detail'),  # GET, PUT, DELETE por ID

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

    # ========== GESTIÓN DE CITAS ==========
    path('citas/', views.lista_citas, name='lista_citas'),
    path('citas/nueva/', views.crear_cita, name='crear_cita'),
    path('citas/editar/<int:pk>/', views.editar_cita, name='editar_cita'),
    path('citas/eliminar/<int:pk>/', views.eliminar_cita, name='eliminar_cita'),
    path('citas/agregar/', views.crear_cita, name='agregar_cita'),  # Alias para consistencia
    path('citas/<int:pk>/', views.detalle_cita, name='detalle_cita'),  # Vista detallada de cita
    
    # ========== GESTIÓN DE TAREAS ==========
    path('tareas/', views.listar_tareas, name='lista_tareas'),
    path('tareas/crear/', views.crear_tarea, name='crear_tarea'),
    path('tareas/editar/<int:tarea_id>/', views.editar_tarea, name='editar_tarea'),
    path('tareas/eliminar/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('tareas/cambiar-estado/<int:tarea_id>/<str:nuevo_estado>/', views.cambiar_estado_tarea, name='cambiar_estado_tarea'),
    
    # ========== GESTIÓN DE SERVICIOS ==========
    path('servicios/lista/', views.servicios_lista, name='servicios-lista'),          # Listar todos los servicios
    path('servicios/crear/', views.servicios_crear, name='servicios-crear'),           # Formulario para crear servicio
    path('servicios/editar/<int:pk>/', views.servicios_editar, name='servicios-editar'),  # Formulario para editar servicio
    path('servicios/eliminar/<int:pk>/', views.servicios_eliminar, name='servicios-eliminar'),  # Confirmación para eliminar servicio

    # ========== GESTIÓN DE CITAS ==========
    path('citas/', views.lista_citas, name='lista_citas'),
    path('citas/nueva/', views.crear_cita, name='crear_cita'),
    path('citas/<int:pk>/editar/', views.editar_cita, name='editar_cita'),
    path('citas/<int:pk>/eliminar/', views.eliminar_cita, name='eliminar_cita'),

    # API para horas disponibles de agenda
    path('api/agenda/horas-disponibles/<str:fecha>/', views.obtener_horas_disponibles, name='obtener_horas_disponibles'),

    # ========== INCLUSIÓN DE ROUTERS ==========
    # Incluye automáticamente las URLs generadas por el router para ViewSets
    # Esto crea URLs como: /agendas/, /agendas/{id}/, /registros/, /registros/{id}/
    path('', include(router.urls)),
]
