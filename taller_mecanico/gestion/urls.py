from django.urls import path
from . import views


urlpatterns = [
    # URLs para la API (sin prefijo 'api/' porque se añade en el proyecto)
    path('clientes/', views.ClienteListCreate.as_view(), name='clientes-list-create'),
    path('clientes/<int:pk>/', views.ClienteRetrieveUpdateDestroy.as_view(), name='cliente-detail'),

    path('empleados/', views.EmpleadoListCreate.as_view(), name='empleados-list-create'),
    path('empleados/<int:pk>/', views.EmpleadoRetrieveUpdateDestroy.as_view(), name='empleado-detail'),

    path('servicios/', views.ServicioListCreate.as_view(), name='servicios-list-create'),
    path('servicios/<int:pk>/', views.ServicioRetrieveUpdateDestroy.as_view(), name='servicio-detail'),

    path('vehiculos/', views.VehiculoListCreate.as_view(), name='vehiculos-list-create'),
    path('vehiculos/<int:pk>/', views.VehiculoRetrieveUpdateDestroy.as_view(), name='vehiculo-detail'),

    path('reparaciones/', views.ReparacionListCreate.as_view(), name='reparaciones-list-create'),
    path('reparaciones/<int:pk>/', views.ReparacionRetrieveUpdateDestroy.as_view(), name='reparacion-detail'),

    # URLs para las vistas de plantilla
    path('clientes/lista/', views.clientes_lista, name='clientes-lista'),
    path('empleados/lista/', views.empleados_lista, name='empleados-lista'),
    path('servicios/lista/', views.servicios_lista, name='servicios-lista'),
]


from rest_framework.routers import DefaultRouter
from .views import AgendaViewSet, RegistroViewSet

router = DefaultRouter()
router.register(r'agendas', AgendaViewSet)
router.register(r'registros', RegistroViewSet)

urlpatterns += router.urls

