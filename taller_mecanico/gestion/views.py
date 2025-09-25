from django.shortcuts import render
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


# --- Vistas de Plantilla ---

def inicio(request):
    return render(request, 'inicio.html')

def clientes_lista(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes_lista.html', {'clientes': clientes})

def empleados_lista(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados_lista.html', {'empleados': empleados})

def servicios_lista(request):
    servicios = Servicio.objects.all()
    return render(request, 'servicios_lista.html', {'servicios': servicios})

    
    
