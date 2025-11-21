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
# Comentado temporalmente hasta que se implementen estos ViewSets
# router.register(r'agendas', views.AgendaViewSet)      # URLs para citas: /agendas/, /agendas/{id}/
# router.register(r'registros', views.RegistroViewSet)  # URLs para registros: /registros/, /registros/{id}/

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
    
    # Dashboard para el mecánico
    path('dashboard-mecanico/', views.dashboard_mecanico, name='dashboard_mecanico'),
    path('mecanico/reparacion/<int:reparacion_id>/', views.gestionar_reparacion_mecanico, name='gestionar_reparacion_mecanico'),
    
    # Gestión de tareas
    path('tareas/', views.listar_tareas, name='listar_tareas'),
    path('tareas/crear/', views.crear_tarea, name='crear_tarea'),
    path('tareas/editar/<int:tarea_id>/', views.editar_tarea, name='editar_tarea'),
    path('tareas/eliminar/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('tareas/cambiar-estado/<int:tarea_id>/<str:nuevo_estado>/', views.cambiar_estado_tarea, name='cambiar_estado_tarea'),
    
    # Dashboard de reparaciones
    path('reparaciones/', views.dashboard_reparaciones, name='dashboard_reparaciones'),
    path('reparaciones/nueva/', views.crear_reparacion, name='crear_reparacion'),
    path('reparaciones/editar/<int:pk>/', views.editar_reparacion, name='editar_reparacion'),
    path('reparaciones/eliminar/<int:pk>/', views.eliminar_reparacion, name='eliminar_reparacion'),
    path('reparaciones/<int:repair_id>/tomar/', views.tomar_reparacion, name='tomar_reparacion'),
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

    # ========== GESTIÓN DE SERVICIOS ==========
    # IMPORTANTE: No eliminar estas URLs - están referenciadas en base.html línea 107
    path('servicios/lista/', views.servicios_lista, name='servicios-lista'),
    path('servicios/crear/', views.servicios_crear, name='servicios-crear'),
    path('servicios/editar/<int:pk>/', views.servicios_editar, name='servicios-editar'),
    path('servicios/eliminar/<int:pk>/', views.servicios_eliminar, name='servicios-eliminar'),

    # ========== GESTIÓN DE CITAS ==========
    # IMPORTANTE: Estas URLs son requeridas por dashboard_encargado.html y dashboard_jefe.html
    # Temporalmente redirigen a not_implemented_view hasta que se implementen
    path('citas/', views.not_implemented_view, name='lista_citas'),
    path('citas/agregar/', views.not_implemented_view, name='agregar_cita'),
    path('citas/crear/', views.not_implemented_view, name='crear_cita'),  # Alias for agregar_cita
    path('citas/<int:pk>/', views.not_implemented_view, name='detalle_cita'),
    path('citas/editar/<int:pk>/', views.not_implemented_view, name='editar_cita'),
    path('citas/eliminar/<int:pk>/', views.not_implemented_view, name='eliminar_cita'),

    # ========== GESTIÓN DE INVENTARIO ==========
    # Comentado temporalmente hasta que se implementen las vistas de inventario
    # path('inventario/', views.inventario_lista, name='inventario-lista'),
    # path('inventario/agregar/', views.inventario_agregar, name='inventario-agregar'),
    # path('inventario/editar/<int:pk>/', views.inventario_editar, name='inventario-editar'),
    # path('inventario/eliminar/<int:pk>/', views.inventario_eliminar, name='inventario-eliminar'),

    # ========== GESTIÓN DE FACTURAS ==========
    # Comentado temporalmente hasta que se implementen las vistas de facturas
    # path('facturas/', views.facturas_lista, name='facturas-lista'),
    # path('facturas/crear/', views.factura_crear, name='factura-crear'),
    # path('facturas/ver/<int:pk>/', views.factura_ver, name='factura-ver'),
    # path('facturas/eliminar/<int:pk>/', views.factura_eliminar, name='factura-eliminar'),

    # ========== GESTIÓN DE REPARACIONES ==========
    path('reparaciones/disponibles/', views.listar_reparaciones_disponibles, name='reparaciones_disponibles'),
    path('reparaciones/<int:reparacion_id>/tomar/', views.tomar_reparacion, name='tomar_reparacion'),
    path('reparaciones/<int:pk>/', views.detalle_reparacion, name='detalle_reparacion'),

    # ========== REPORTES ==========
    # Comentado temporalmente hasta que se implementen las vistas de reportes
    # path('reportes/', views.reportes, name='reportes'),
    # path('reportes/ventas/', views.reporte_ventas, name='reporte-ventas'),
    # path('reportes/inventario/', views.reporte_inventario, name='reporte-inventario'),
    # path('reportes/ingresos/', views.reportes_ingresos, name='reporte-ingresos'),
    # path('reportes/ingresos/exportar/', views.exportar_ingresos_excel, name='exportar-ingresos-excel'),
    # path('ajax/load-precio-servicio/', views.ajax_load_precio_servicio, name='ajax-load-precio-servicio'),

    # ========== OTRAS RUTAS ==========
    path('', views.inicio, name='home'),  # Ruta raíz que redirige al inicio
    # Comentado temporalmente hasta que se implementen las vistas
    # path('acerca-de/', views.acerca_de, name='acerca-de'),
    # path('contacto/', views.contacto, name='contacto'),
    
    # ========== GESTIÓN DE CITAS ==========
    # Comentado temporalmente hasta que se implementen las vistas de citas
    # path('citas/', views.lista_citas, name='lista_citas'),
    # path('citas/nueva/', views.crear_cita, name='crear_cita'),
    # path('citas/<int:pk>/editar/', views.editar_cita, name='editar_cita'),
    # path('citas/<int:pk>/eliminar/', views.eliminar_cita, name='eliminar_cita'),

    # API para horas disponibles de agenda
    # path('api/agenda/horas-disponibles/<str:fecha>/', views.obtener_horas_disponibles, name='obtener_horas_disponibles'),

    # ========== INCLUSIÓN DE ROUTERS ==========
    # Incluye automáticamente las URLs generadas por el router para ViewSets
    # Esto crea URLs como: /agendas/, /agendas/{id}/, /registros/, /registros/{id}/
    path('', include(router.urls)),
]
