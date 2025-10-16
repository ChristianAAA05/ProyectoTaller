from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from .decorators import jefe_required, empleados_management_required, servicios_management_required
from .forms import ClienteForm, EmpleadoForm, ServicioForm
from .models import (
    Cliente, Empleado, Servicio, Vehiculo, Reparacion, Agenda, Registro
)
from .serializers import (
    ClienteSerializer, EmpleadoSerializer, ServicioSerializer,
    VehiculoSerializer, ReparacionSerializer, AgendaSerializer, RegistroSerializer
)

# Create your views here.

# --- Vistas de Autenticación ---

def login_view(request):
    """Vista de login personalizado"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}!')
            
            # Redirigir según el tipo de usuario
            if hasattr(user, 'profile') and user.profile.es_empleado:
                return redirect('inicio')
            else:
                return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'auth/login.html')


def logout_view(request):
    """Vista de logout"""
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')


@login_required
def perfil_view(request):
    """Vista de perfil de usuario"""
    return render(request, 'auth/perfil.html', {'user': request.user})


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

# ViewSets con validaciones personalizadas
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

@login_required
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


@login_required
def clientes_lista(request):
    """Lista de clientes"""
    clientes = Cliente.objects.all()
    return render(request, 'clientes_lista.html', {'clientes': clientes})


@login_required
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


@login_required
def servicios_lista(request):
    """Lista de servicios"""
    servicios = Servicio.objects.all()
    return render(request, 'servicios_lista.html', {'servicios': servicios})


@login_required
@jefe_required
def clientes_crear(request):
    """Crear nuevo cliente usando ModelForm"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            try:
                cliente = form.save()
                messages.success(request, f'Cliente "{cliente.nombre}" creado exitosamente.')
                return redirect('clientes-lista')
            except Exception as e:
                messages.error(request, f'Error al crear cliente: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = ClienteForm()

    context = {
        'form': form,
        'accion': 'Crear'
    }
    return render(request, 'clientes_form.html', context)


@login_required
@jefe_required
def clientes_editar(request, pk):
    """Editar cliente existente usando ModelForm"""
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            try:
                cliente_actualizado = form.save()
                messages.success(request, f'Cliente "{cliente_actualizado.nombre}" actualizado exitosamente.')
                return redirect('clientes-lista')
            except Exception as e:
                messages.error(request, f'Error al actualizar cliente: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = ClienteForm(instance=cliente)

    context = {
        'form': form,
        'cliente': cliente,
        'accion': 'Editar'
    }
    return render(request, 'clientes_form.html', context)


@login_required
@jefe_required
def clientes_eliminar(request, pk):
    """Eliminar cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        try:
            nombre = cliente.nombre
            cliente.delete()
            messages.success(request, f'Cliente "{nombre}" eliminado exitosamente.')
            return redirect('clientes-lista')
        except Exception as e:
            messages.error(request, f'Error al eliminar cliente: {str(e)}')

    context = {'cliente': cliente}
    return render(request, 'clientes_confirm_delete.html', context)


@login_required
@empleados_management_required
def empleados_crear(request):
    """Crear nuevo empleado usando ModelForm"""
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            try:
                empleado = form.save()
                messages.success(request, f'Empleado "{empleado.nombre}" creado exitosamente.')
                return redirect('empleados-lista')
            except Exception as e:
                messages.error(request, f'Error al crear empleado: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = EmpleadoForm()

    context = {
        'form': form,
        'accion': 'Crear'
    }
    return render(request, 'empleados_form.html', context)


@login_required
@empleados_management_required
def empleados_editar(request, pk):
    """Editar empleado existente usando ModelForm"""
    empleado = get_object_or_404(Empleado, pk=pk)

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            try:
                empleado_actualizado = form.save()
                messages.success(request, f'Empleado "{empleado_actualizado.nombre}" actualizado exitosamente.')
                return redirect('empleados-lista')
            except Exception as e:
                messages.error(request, f'Error al actualizar empleado: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = EmpleadoForm(instance=empleado)

    context = {
        'form': form,
        'empleado': empleado,
        'accion': 'Editar'
    }
    return render(request, 'empleados_form.html', context)


@login_required
@empleados_management_required
def empleados_eliminar(request, pk):
    """Eliminar empleado"""
    empleado = get_object_or_404(Empleado, pk=pk)

    if request.method == 'POST':
        try:
            nombre = empleado.nombre
            empleado.delete()
            messages.success(request, f'Empleado "{nombre}" eliminado exitosamente.')
            return redirect('empleados-lista')
        except Exception as e:
            messages.error(request, f'Error al eliminar empleado: {str(e)}')

    context = {'empleado': empleado}
    return render(request, 'empleados_confirm_delete.html', context)


@login_required
@servicios_management_required
def servicios_crear(request):
    """Crear nuevo servicio usando ModelForm"""
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            try:
                servicio = form.save()
                messages.success(request, f'Servicio "{servicio.nombre_servicio}" creado exitosamente.')
                return redirect('servicios-lista')
            except Exception as e:
                messages.error(request, f'Error al crear servicio: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = ServicioForm()

    context = {
        'form': form,
        'accion': 'Crear'
    }
    return render(request, 'servicios_form.html', context)


@login_required
@servicios_management_required
def servicios_editar(request, pk):
    """Editar servicio existente usando ModelForm"""
    servicio = get_object_or_404(Servicio, pk=pk)

    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            try:
                servicio_actualizado = form.save()
                messages.success(request, f'Servicio "{servicio_actualizado.nombre_servicio}" actualizado exitosamente.')
                return redirect('servicios-lista')
            except Exception as e:
                messages.error(request, f'Error al actualizar servicio: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = ServicioForm(instance=servicio)

    context = {
        'form': form,
        'servicio': servicio,
        'accion': 'Editar'
    }
    return render(request, 'servicios_form.html', context)


@login_required
@servicios_management_required
def servicios_eliminar(request, pk):
    """Eliminar servicio"""
    servicio = get_object_or_404(Servicio, pk=pk)

    if request.method == 'POST':
        try:
            nombre = servicio.nombre_servicio
            servicio.delete()
            messages.success(request, f'Servicio "{nombre}" eliminado exitosamente.')
            return redirect('servicios-lista')
        except Exception as e:
            messages.error(request, f'Error al eliminar servicio: {str(e)}')

    context = {'servicio': servicio}
    return render(request, 'servicios_confirm_delete.html', context)

# --- Funciones de utilidad para permisos ---

def es_jefe(user):
    """Verifica si el usuario es jefe (tiene permisos completos)"""
    try:
        return not user.profile.es_empleado or user.profile.empleado_relacionado.puesto.lower() == 'jefe'
    except:
        return False

def es_encargado(user):
    """Verifica si el usuario es un encargado con permisos limitados"""
    try:
        return (user.profile.es_empleado and
                user.profile.empleado_relacionado.puesto.lower() in ['encargado', 'supervisor'])
    except:
        return False

def puede_gestionar_empleados(user):
    """Verifica si el usuario puede gestionar empleados (agregar/editar/eliminar)"""
    return es_jefe(user)

def puede_gestionar_servicios(user):
    """Verifica si el usuario puede gestionar servicios (agregar/editar/eliminar)"""
    return es_jefe(user)

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

class APIAuthenticationMixin:
    """Mixin para agregar autenticación a las vistas de API"""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

# Aplicar autenticación a todas las vistas de API
ClienteListCreate.authentication_classes = [SessionAuthentication]
ClienteListCreate.permission_classes = [IsAuthenticated]
ClienteRetrieveUpdateDestroy.authentication_classes = [SessionAuthentication]
ClienteRetrieveUpdateDestroy.permission_classes = [IsAuthenticated]

EmpleadoListCreate.authentication_classes = [SessionAuthentication]
EmpleadoListCreate.permission_classes = [IsAuthenticated]
EmpleadoRetrieveUpdateDestroy.authentication_classes = [SessionAuthentication]
EmpleadoRetrieveUpdateDestroy.permission_classes = [IsAuthenticated]

ServicioListCreate.authentication_classes = [SessionAuthentication]
ServicioListCreate.permission_classes = [IsAuthenticated]
ServicioRetrieveUpdateDestroy.authentication_classes = [SessionAuthentication]
ServicioRetrieveUpdateDestroy.permission_classes = [IsAuthenticated]

VehiculoListCreate.authentication_classes = [SessionAuthentication]
VehiculoListCreate.permission_classes = [IsAuthenticated]
VehiculoRetrieveUpdateDestroy.authentication_classes = [SessionAuthentication]
VehiculoRetrieveUpdateDestroy.permission_classes = [IsAuthenticated]

ReparacionListCreate.authentication_classes = [SessionAuthentication]
ReparacionListCreate.permission_classes = [IsAuthenticated]
ReparacionRetrieveUpdateDestroy.authentication_classes = [SessionAuthentication]
ReparacionRetrieveUpdateDestroy.permission_classes = [IsAuthenticated]

AgendaViewSet.authentication_classes = [SessionAuthentication]
AgendaViewSet.permission_classes = [IsAuthenticated]
RegistroViewSet.authentication_classes = [SessionAuthentication]
RegistroViewSet.permission_classes = [IsAuthenticated]
