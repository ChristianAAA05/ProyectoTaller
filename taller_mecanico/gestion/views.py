from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db.models.functions import ExtractMonth, ExtractYear

from .decorators import jefe_required, empleados_management_required, servicios_management_required
from .forms import ClienteForm, EmpleadoForm, ServicioForm, VehiculoForm
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
    """
    Redirige al usuario al dashboard correspondiente según su rol.
    """
    if hasattr(request.user, 'profile') and request.user.profile.es_empleado:
        # Verificar si es jefe
        if es_jefe(request.user):
            return redirect('dashboard_jefe')
        # Si no es jefe, es encargado
        return redirect('dashboard_encargado')
    
    # Si es cliente, redirigir al dashboard de cliente
    return redirect('dashboard_cliente')

@login_required
@jefe_required
def dashboard_jefe(request):
    """Dashboard exclusivo para el jefe del taller"""
    from django.utils import timezone
    from django.db.models import Count, Q, Sum, F, Case, When, IntegerField
    
    # Obtener la fecha actual
    hoy = timezone.now().date()
    
    # Estadísticas generales
    total_clientes = Cliente.objects.count()
    total_empleados = Empleado.objects.count()
    total_servicios = Servicio.objects.count()
    total_vehiculos = Vehiculo.objects.count()
    
    # Reparaciones
    reparaciones = Reparacion.objects.all()
    total_reparaciones = reparaciones.count()
    reparaciones_pendientes = reparaciones.filter(estado='Pendiente').count()
    reparaciones_en_proceso = reparaciones.filter(estado='En Proceso').count()
    reparaciones_completadas = reparaciones.filter(estado='Completada').count()
    
    # Reparaciones recientes (últimas 5)
    reparaciones_recientes = reparaciones.select_related('vehiculo', 'servicio').order_by('-fecha_ingreso')[:5]
    
    # Citas
    citas = Agenda.objects.all()
    total_citas = citas.count()
    
    # Citas de hoy
    citas_hoy = citas.filter(fecha=hoy).order_by('hora')
    
    # Próximas citas (próximos 7 días)
    proxima_semana = hoy + timezone.timedelta(days=7)
    citas_proximas = citas.filter(
        fecha__range=[hoy, proxima_semana]
    ).order_by('fecha', 'hora')[:10]
    
    # Empleados destacados (versión simplificada temporalmente)
    # Primero obtenemos todos los empleados
    empleados_destacados = Empleado.objects.all()[:5]  # Mostrar primeros 5 empleados
    
    # Agregamos manualmente el conteo de reparaciones
    desde = timezone.now() - timezone.timedelta(days=30)
    for empleado in empleados_destacados:
        # Contar registros de este empleado en el último mes
        empleado.num_reparaciones = Registro.objects.filter(
            empleado=empleado,
            fecha__gte=desde
        ).count()
    
    # Reparaciones por estado (para gráfico)
    estados_reparacion = ['Pendiente', 'En Proceso', 'Completada', 'Cancelada']
    reparaciones_por_estado = []
    for estado in estados_reparacion:
        count = reparaciones.filter(estado=estado).count()
        reparaciones_por_estado.append({
            'estado': estado,
            'total': count,
            'porcentaje': round((count / total_reparaciones * 100) if total_reparaciones > 0 else 0, 1)
        })
    
    # Ingresos mensuales (últimos 6 meses)
    seis_meses_atras = hoy - timezone.timedelta(days=180)
    # Versión simplificada temporalmente - mostrar solo el conteo de reparaciones
    ingresos_mensuales = Reparacion.objects.filter(
        fecha_ingreso__gte=seis_meses_atras,
        estado='Completada'
    ).annotate(
        mes=ExtractMonth('fecha_ingreso'),
        anio=ExtractYear('fecha_ingreso')
    ).values('anio', 'mes').annotate(
        total=Count('id')
    ).order_by('anio', 'mes')
    
    # Preparar datos para la gráfica de ingresos
    meses = []
    ingresos = []
    for ingreso in ingresos_mensuales:
        meses.append(f"{ingreso['mes']}/{ingreso['anio']}")
        ingresos.append(float(ingreso['total'] or 0))
    
    context = {
        'titulo': 'Panel del Jefe',
        'es_jefe': True,
        'es_encargado': False,
        'hoy': hoy,
        
        # Estadísticas generales
        'total_clientes': total_clientes,
        'total_empleados': total_empleados,
        'total_servicios': total_servicios,
        'total_vehiculos': total_vehiculos,
        'total_reparaciones': total_reparaciones,
        'total_citas': total_citas,
        
        # Datos de reparaciones
        'reparaciones_pendientes': reparaciones_pendientes,
        'reparaciones_en_proceso': reparaciones_en_proceso,
        'reparaciones_completadas': reparaciones_completadas,
        'reparaciones_recientes': reparaciones_recientes,
        'reparaciones_por_estado': reparaciones_por_estado,
        
        # Datos de citas
        'citas_hoy': citas_hoy,
        'citas_proximas': citas_proximas,
        
        # Empleados
        'empleados_destacados': empleados_destacados,
        
        # Datos para gráficos
        'meses_ingresos': meses,
        'ingresos': ingresos,
    }
    
    return render(request, 'gestion/dashboard_jefe.html', context)

@login_required
def dashboard_encargado(request):
    """Dashboard para encargados del taller"""
    from django.utils import timezone
    from django.db.models import Count, Q
    
    hoy = timezone.now().date()
    
    # Citas de hoy
    citas_hoy = Agenda.objects.filter(
        fecha=hoy
    ).select_related('cliente', 'servicio').order_by('hora')
    
    # Reparaciones en progreso o pendientes
    reparaciones_en_progreso = Reparacion.objects.filter(
        estado__in=['En progreso', 'Pendiente']
    ).select_related('vehiculo', 'servicio').order_by('fecha_ingreso')[:10]
    
    # Próximas citas (próximos 3 días)
    proximos_dias = hoy + timezone.timedelta(days=3)
    proximas_citas = Agenda.objects.filter(
        fecha__range=[hoy, proximos_dias]
    ).select_related('cliente', 'servicio').order_by('fecha', 'hora')[:5]
    
    # Estadísticas rápidas
    total_citas_hoy = citas_hoy.count()
    reparaciones_pendientes = Reparacion.objects.filter(
        estado__in=['En progreso', 'Pendiente']
    ).count()
    
    context = {
        'titulo': 'Panel del Encargado',
        'es_jefe': False,
        'es_encargado': True,
        'hoy': hoy,
        'es_jefe': False,
        'es_encargado': True,
        'citas_hoy': citas_hoy,
        'reparaciones_en_progreso': reparaciones_en_progreso,
    }
    
    return render(request, 'gestion/dashboard_encargado.html', context)

@login_required
def dashboard_cliente(request):
    """
    Dashboard personalizado para clientes del taller.
    Muestra información relevante sobre sus vehículos, citas y reparaciones.
    """
    from django.utils import timezone
    
    # Obtener el perfil del cliente
    try:
        perfil = request.user.profile
        cliente = Cliente.objects.get(correo_electronico=request.user.email)
    except (UserProfile.DoesNotExist, Cliente.DoesNotExist):
        # Si no existe el perfil o el cliente, redirigir a completar registro
        messages.info(request, 'Por favor, complete su perfil de cliente')
        return redirect('completar_perfil')
    
    # Obtener los vehículos del cliente
    vehiculos = Vehiculo.objects.filter(cliente=cliente)
    
    # Obtener las reparaciones recientes (últimos 3 meses)
    tres_meses_atras = timezone.now() - timezone.timedelta(days=90)
    reparaciones = Reparacion.objects.filter(
        vehiculo__in=vehiculos,
        fecha_ingreso__gte=tres_meses_atras
    ).select_related('vehiculo', 'servicio').order_by('-fecha_ingreso')[:5]
    
    # Obtener citas programadas (futuras y de hoy)
    hoy = timezone.now().date()
    citas = Agenda.objects.filter(
        cliente=cliente,
        fecha__gte=hoy
    ).select_related('servicio').order_by('fecha', 'hora')
    
    # Obtener vehículos con reparaciones recientes
    vehiculos_con_reparaciones = []
    for vehiculo in vehiculos:
        ultima_reparacion = Reparacion.objects.filter(
            vehiculo=vehiculo
        ).order_by('-fecha_ingreso').first()
        vehiculos_con_reparaciones.append({
            'vehiculo': vehiculo,
            'ultima_reparacion': ultima_reparacion
        })
    
    # Estadísticas rápidas
    total_vehiculos = vehiculos.count()
    total_reparaciones = Reparacion.objects.filter(
        vehiculo__in=vehiculos
    ).count()
    total_citas_pendientes = citas.count()
    
    context = {
        'titulo': 'Mi Espacio Cliente',
        'cliente': cliente,
        'vehiculos': vehiculos_con_reparaciones,
        'reparaciones': reparaciones,
        'citas': citas,
        'total_vehiculos': total_vehiculos,
        'total_reparaciones': total_reparaciones,
        'total_citas_pendientes': total_citas_pendientes,
        'hoy': hoy,
    }
    
    return render(request, 'gestion/dashboard_cliente.html', context)


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
    """Crear nuevo cliente con vehículos usando ModelForm y formsets"""
    VehiculoFormSet = formset_factory(VehiculoForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        formset = VehiculoFormSet(request.POST, prefix='vehiculos')

        if form.is_valid() and formset.is_valid():
            try:
                # Crear el cliente primero
                cliente = form.save()

                # Crear los vehículos asociados
                for vehiculo_form in formset:
                    if vehiculo_form.cleaned_data.get('marca'):  # Solo si tiene datos
                        vehiculo = vehiculo_form.save(commit=False)
                        vehiculo.cliente = cliente
                        vehiculo.save()

                messages.success(request, f'Cliente "{cliente.nombre}" creado exitosamente con {formset.total_form_count()} vehículo(s).')
                return redirect('clientes-lista')

            except Exception as e:
                messages.error(request, f'Error al crear cliente: {str(e)}')
        else:
            # Mostrar errores específicos
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Cliente - {field}: {error}')

            for i, vehiculo_form in enumerate(formset):
                if vehiculo_form.errors:
                    for field, errors in vehiculo_form.errors.items():
                        for error in errors:
                            messages.error(request, f'Vehículo {i+1} - {field}: {error}')

            if formset.non_form_errors():
                for error in formset.non_form_errors():
                    messages.error(request, f'Vehículo: {error}')
    else:
        form = ClienteForm()
        formset = VehiculoFormSet(prefix='vehiculos')

    context = {
        'form': form,
        'formset': formset,
        'accion': 'Crear'
    }
    return render(request, 'clientes_form.html', context)


@login_required
@jefe_required
def clientes_editar(request, pk):
    """Editar cliente existente con vehículos usando ModelForm y formsets"""
    cliente = get_object_or_404(Cliente, pk=pk)
    VehiculoFormSet = formset_factory(VehiculoForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        formset = VehiculoFormSet(request.POST, prefix='vehiculos')

        if form.is_valid() and formset.is_valid():
            try:
                # Guardar el cliente primero
                cliente_actualizado = form.save()

                # Eliminar vehículos marcados para eliminación
                for vehiculo_form in formset:
                    if vehiculo_form.cleaned_data.get('DELETE', False):
                        vehiculo_id = vehiculo_form.cleaned_data.get('id')
                        if vehiculo_id:
                            vehiculo_id.delete()

                # Crear/actualizar vehículos
                for vehiculo_form in formset:
                    if vehiculo_form.cleaned_data.get('marca') and not vehiculo_form.cleaned_data.get('DELETE', False):
                        vehiculo = vehiculo_form.save(commit=False)
                        if hasattr(vehiculo_form, 'instance') and vehiculo_form.instance.pk:
                            # Actualizar vehículo existente
                            vehiculo.pk = vehiculo_form.instance.pk
                        vehiculo.cliente = cliente_actualizado
                        vehiculo.save()

                messages.success(request, f'Cliente "{cliente_actualizado.nombre}" actualizado exitosamente.')
                return redirect('clientes-lista')

            except Exception as e:
                messages.error(request, f'Error al actualizar cliente: {str(e)}')
        else:
            # Mostrar errores específicos
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Cliente - {field}: {error}')

            for i, vehiculo_form in enumerate(formset):
                if vehiculo_form.errors:
                    for field, errors in vehiculo_form.errors.items():
                        for error in errors:
                            messages.error(request, f'Vehículo {i+1} - {field}: {error}')

            if formset.non_form_errors():
                for error in formset.non_form_errors():
                    messages.error(request, f'Vehículo: {error}')
    else:
        form = ClienteForm(instance=cliente)
        # Crear formset con vehículos existentes
        vehiculos_existentes = cliente.vehiculos.all()
        formset = VehiculoFormSet(
            prefix='vehiculos',
            initial=[{'marca': v.marca, 'modelo': v.modelo, 'año': v.año, 'placa': v.placa} for v in vehiculos_existentes]
        )

    context = {
        'form': form,
        'cliente': cliente,
        'formset': formset,
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
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
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
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
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
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
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
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
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
