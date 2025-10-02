from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from .models import Cliente, Empleado, Servicio, Vehiculo, Reparacion, Agenda, Registro
from .serializers import (
    ClienteSerializer, EmpleadoSerializer, ServicioSerializer, 
    VehiculoSerializer, ReparacionSerializer, AgendaSerializer, RegistroSerializer
)

# Create your views here.

# --- Vistas de la API ---

# Cliente
class ClienteListCreate(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ClienteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

# Empleado
class EmpleadoListCreate(generics.ListCreateAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class EmpleadoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

# Servicio
class ServicioListCreate(generics.ListCreateAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class ServicioRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

# Vehiculo
class VehiculoListCreate(generics.ListCreateAPIView):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class VehiculoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

# Reparacion
class ReparacionListCreate(generics.ListCreateAPIView):
    queryset = Reparacion.objects.all()
    serializer_class = ReparacionSerializer

class ReparacionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reparacion.objects.all()
    serializer_class = ReparacionSerializer

# Agenda
class AgendaListCreate(generics.ListCreateAPIView):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

class AgendaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

# Registro
class RegistroListCreate(generics.ListCreateAPIView):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer

class RegistroRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer


# --- Vistas basadas en plantillas ---

def inicio(request):
    """Vista principal del taller mecánico"""
    from django.utils import timezone
    total_clientes = Cliente.objects.count()
    total_empleados = Empleado.objects.count()
    total_servicios = Servicio.objects.count()
    total_vehiculos = Vehiculo.objects.count()
    reparaciones_pendientes = Reparacion.objects.filter(estado='En progreso').count()
    citas_hoy = Agenda.objects.filter(
        fecha_hora__date=timezone.now().date()
    ).count()

    context = {
        'total_clientes': total_clientes,
        'total_empleados': total_empleados,
        'total_servicios': total_servicios,
        'total_vehiculos': total_vehiculos,
        'reparaciones_pendientes': reparaciones_pendientes,
        'citas_hoy': citas_hoy,
    }
    return render(request, 'inicio.html', context)

def clientes_lista(request):
    """Lista de clientes"""
    clientes = Cliente.objects.all()
    return render(request, 'clientes_lista.html', {'clientes': clientes})

def empleados_lista(request):
    """Lista de empleados"""
    empleados = Empleado.objects.all()
    context = {
        'empleados': empleados,
        'puestos': Empleado.objects.values_list('puesto', flat=True).distinct()
    }
    return render(request, 'empleados_lista.html', context)

def servicios_lista(request):
    """Lista de servicios"""
    servicios = Servicio.objects.all()
    return render(request, 'servicios_lista.html', {'servicios': servicios})
