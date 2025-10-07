from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from django.core.exceptions import ValidationError
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

# # Agenda
# class AgendaListCreate(generics.ListCreateAPIView):
#     queryset = Agenda.objects.all()
#     serializer_class = AgendaSerializer

# class AgendaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Agenda.objects.all()
#     serializer_class = AgendaSerializer

# # Registro
# class RegistroListCreate(generics.ListCreateAPIView):
#     queryset = Registro.objects.all()
#     serializer_class = RegistroSerializer

# class RegistroRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Registro.objects.all()
#     serializer_class = RegistroSerializer


from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Agenda, Registro
from .serializers import AgendaSerializer, RegistroSerializer

class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            cita = Agenda().programarCita(
                cliente=serializer.validated_data['cliente'],
                servicio=serializer.validated_data['servicio'],
                fecha=serializer.validated_data['fecha'],
                hora=serializer.validated_data['hora']
            )
        except ValidationError as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        output_serializer = self.get_serializer(cita)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class RegistroViewSet(viewsets.ModelViewSet):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            registro = Registro().crearRegistro(
                cliente = serializer.validated_data['cliente'],
                empleado = serializer.validated_data['empleado'],
                servicio = serializer.validated_data['servicio'],
                fecha = serializer.validated_data.get('fecha', None)
            )
        except ValidationError as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        output_serializer = self.get_serializer(registro)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


# --- Vistas basadas en plantillas ---

def inicio(request):
    """Vista principal del taller mecánico"""
    from django.utils import timezone

    # Obtener métricas con manejo de errores
    total_clientes = Cliente.objects.count()
    total_vehiculos = Vehiculo.objects.count()
    reparaciones_pendientes = Reparacion.objects.filter(estado='En progreso').count()
    citas_hoy = Agenda.objects.filter(
        fecha=timezone.now().date()
    ).count()

    # Obtener empleados con manejo de errores
    try:
        total_empleados = Empleado.objects.count()
        empleados_for_services = Empleado.objects.values_list('puesto', flat=True).distinct()
    except Exception:
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM gestion_empleado")
                total_empleados = cursor.fetchone()[0]
                cursor.execute("SELECT DISTINCT puesto FROM gestion_empleado")
                empleados_for_services = [row[0] for row in cursor.fetchall() if row[0]]
        except Exception:
            total_empleados = 0
            empleados_for_services = []

    # Obtener servicios con manejo de errores
    try:
        total_servicios = Servicio.objects.count()
    except Exception:
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM gestion_servicio")
                total_servicios = cursor.fetchone()[0]
        except Exception:
            total_servicios = 0

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
    try:
        empleados = Empleado.objects.all()
        empleados_lista = list(empleados)  # Forzar evaluación del QuerySet
        context = {
            'empleados': empleados_lista,
            'puestos': Empleado.objects.values_list('puesto', flat=True).distinct()
        }
    except Exception as e:
        # Si hay error con el ORM, intentar consulta directa
        empleados_lista = []
        puestos = []
        error_msg = f"Error con empleados: {str(e)}"

        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre, puesto, telefono, correo_electronico FROM gestion_empleado")
                empleados_raw = cursor.fetchall()

                # Crear objetos Empleado manualmente
                for emp_data in empleados_raw:
                    class EmpleadoTemp:
                        def __init__(self, nombre, puesto, telefono, correo):
                            self.nombre = nombre
                            self.puesto = puesto
                            self.telefono = telefono
                            self.correo_electronico = correo

                        def __str__(self):
                            return self.nombre

                    empleados_lista.append(EmpleadoTemp(*emp_data))

                # Obtener puestos únicos
                cursor.execute("SELECT DISTINCT puesto FROM gestion_empleado")
                puestos_raw = cursor.fetchall()
                puestos = [puesto[0] for puesto in puestos_raw if puesto[0]]

        except Exception as db_error:
            error_msg += f" | Error DB: {str(db_error)}"

        context = {
            'empleados': empleados_lista,
            'puestos': puestos,
            'error': error_msg
        }

    return render(request, 'empleados_lista.html', context)

def servicios_lista(request):
    """Lista de servicios"""
    servicios = Servicio.objects.all()
    return render(request, 'servicios_lista.html', {'servicios': servicios})
