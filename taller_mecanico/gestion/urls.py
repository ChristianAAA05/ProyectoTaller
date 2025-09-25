from django.urls import path
from . import views


urlpatterns = [
    # URLs para la API
    path('api/clientes/', views.ClienteListCreate.as_view(), name='clientes-list-create'),
    path('api/clientes/<int:pk>/', views.ClienteRetrieveUpdateDestroy.as_view(), name='cliente-detail'),
    
    path('api/empleados/', views.EmpleadoListCreate.as_view(), name='empleados-list-create'),
    path('api/empleados/<int:pk>/', views.EmpleadoRetrieveUpdateDestroy.as_view(), name='empleado-detail'),

    path('api/servicios/', views.ServicioListCreate.as_view(), name='servicios-list-create'),
    path('api/servicios/<int:pk>/', views.ServicioRetrieveUpdateDestroy.as_view(), name='servicio-detail'),

    path('api/vehiculos/', views.VehiculoListCreate.as_view(), name='vehiculos-list-create'),
    path('api/vehiculos/<int:pk>/', views.VehiculoRetrieveUpdateDestroy.as_view(), name='vehiculo-detail'),

    path('api/reparaciones/', views.ReparacionListCreate.as_view(), name='reparaciones-list-create'),
    path('api/reparaciones/<int:pk>/', views.ReparacionRetrieveUpdateDestroy.as_view(), name='reparacion-detail'),

    path('api/agendas/', views.AgendaListCreate.as_view(), name='agendas-list-create'),
    path('api/agendas/<int:pk>/', views.AgendaRetrieveUpdateDestroy.as_view(), name='agenda-detail'),

    path('api/registros/', views.RegistroListCreate.as_view(), name='registros-list-create'),
    path('api/registros/<int:pk>/', views.RegistroRetrieveUpdateDestroy.as_view(), name='registro-detail'),

    # URLs para las vistas de plantilla
    path('clientes/lista/', views.clientes_lista, name='clientes-lista'),
    path('empleados/lista/', views.empleados_lista, name='empleados-lista'),
    path('servicios/lista/', views.servicios_lista, name='servicios-lista'),
]



