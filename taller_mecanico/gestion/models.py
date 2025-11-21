"""
Modelos de la aplicación Taller Mecánico

Este archivo define todos los modelos de datos utilizados en el sistema:
- UserProfile: Perfil extendido de usuario con información adicional
- Cliente: Información de clientes del taller
- Empleado: Información de empleados del taller
- Servicio: Servicios ofrecidos por el taller
- Vehiculo: Vehículos de los clientes
- Reparacion: Registro de reparaciones realizadas
- Agenda: Sistema de citas y agendamiento
- Registro: Historial de servicios realizados

Cada modelo incluye métodos __str__ para representación legible y métodos
personalizados para operaciones específicas del negocio.
"""

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Modelo de Perfil de usuario personalizado
# Extiende el modelo User de Django con información adicional específica del taller
class UserProfile(models.Model):
    """
    Perfil extendido de usuario que añade información específica del taller.

    Relaciona cada usuario con información adicional como teléfono, dirección,
    avatar y determina si es empleado del taller o cliente externo.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    avatar_url = models.URLField(max_length=500, blank=True, null=True, help_text="URL de la imagen de avatar")
    es_empleado = models.BooleanField(default=False)
    empleado_relacionado = models.OneToOneField('Empleado', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

    def save(self, *args, **kwargs):
        # Si es empleado, conectar automáticamente con el modelo Empleado
        # Busca un empleado con el mismo correo electrónico del usuario
        if self.es_empleado and not self.empleado_relacionado:
            try:
                empleado = Empleado.objects.get(correo_electronico=self.user.email)
                self.empleado_relacionado = empleado
            except Empleado.DoesNotExist:
                # Si no existe empleado con ese email, continúa sin asociar
                pass
        super().save(*args, **kwargs)

# ========== MODELOS PRINCIPALES DEL NEGOCIO ==========

class Cliente(models.Model):
    """
    Modelo que representa a los clientes del taller mecánico.

    Contiene información básica de contacto y permite relacionar múltiples vehículos.
    """
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)  # Campo agregado en migración
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)
    correo_electronico = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(default=timezone.now, verbose_name='Fecha de registro')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

class Empleado(models.Model):
    """
    Modelo que representa a los empleados del taller mecánico.

    Define diferentes puestos de Trabajo y permite gestionar el personal.
    """
    nombre = models.CharField(max_length=100)
    puesto = models.CharField(max_length=50)  # Jefe, Mecánico, Recepcionista, etc.
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "empleado"
        verbose_name_plural = "Empleados"

class Servicio(models.Model):
    """
    Modelo que representa los servicios ofrecidos por el taller.

    Define el catálogo de servicios disponibles con precios y duración estimada.
    """
    nombre_servicio = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del servicio
    duracion = models.IntegerField()  # Duración en minutos

    def __str__(self):
        return self.nombre_servicio

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

class Vehiculo(models.Model):
    """
    Modelo que representa los vehículos de los clientes.

    Cada vehículo pertenece a un cliente específico y puede tener múltiples reparaciones.
    """
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vehiculos')
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    año = models.IntegerField()
    placa = models.CharField(max_length=10, unique=True)  # Placa única del vehículo

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"

class Reparacion(models.Model):
    """
    Modelo que registra las reparaciones realizadas en el taller.

    Relaciona vehículos con servicios específicos y permite rastrear el estado
    y progreso de cada reparación.
    """
    # Estados de condición del vehículo
    CONDICION_OPCIONES = [
        ('excelente', 'Excelente - Vehículo como nuevo, solo mantenimiento preventivo'),
        ('bueno', 'Bueno - Desgaste leve, puede necesitar ajustes menores'),
        ('regular', 'Regular - Desgaste notable, necesita reparaciones moderadas'),
        ('malo', 'Malo - Desgastado, necesita reparaciones extensas'),
        ('critico', 'Crítico - Daño estructural, posible pérdida total'),
    ]
    
    # Estados de la reparación
    ESTADO_REPARACION = [
        ('pendiente', '🟡 Pendiente'),
        ('en_progreso', '🔵 En Progreso'),
        ('en_espera', '🟠 En Espera de Repuestos'),
        ('revision', '🟣 Lista para Revisión'),
        ('completada', '🟢 Completada'),
        ('cancelada', '🔴 Cancelada'),
    ]
    
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='reparaciones')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    mecanico_asignado = models.ForeignKey(
        'Empleado', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reparaciones_asignadas',
        verbose_name='Mecánico Asignado',
        help_text='Mecánico responsable de la reparación'
    )
    fecha_ingreso = models.DateTimeField(auto_now_add=True)  # Fecha automática de ingreso
    fecha_salida = models.DateTimeField(null=True, blank=True)  # Fecha de entrega
    condicion_vehiculo = models.CharField(
        max_length=20, 
        choices=CONDICION_OPCIONES, 
        default='regular',
        verbose_name='Condición del Vehículo',
        help_text="Estado general del vehículo que determina el tipo de reparación necesaria"
    )
    estado_reparacion = models.CharField(
        max_length=20,
        choices=ESTADO_REPARACION,
        default='pendiente',
        verbose_name='Estado de la Reparación',
        help_text="Estado actual de la reparación"
    )
    notas = models.TextField(blank=True, null=True, help_text="Notas adicionales sobre la reparación")

    def __str__(self):
        return f"Reparación de {self.vehiculo} - {self.servicio}"

    class Meta:
        verbose_name = "Reparación"
        verbose_name_plural = "Reparaciones"

class Agenda(models.Model):
    """
    Modelo para gestionar citas y agendamiento de servicios.

    Permite programar citas futuras y evitar conflictos de horario.
    """
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"Cita para {self.cliente} - {self.servicio} el {self.fecha} a las {self.hora}"

    def programarCita(self, cliente, servicio, fecha, hora):
        """
        Método personalizado para programar citas con validaciones.

        Verifica que la fecha no sea pasada y que no haya conflictos de horario.
        """
        # Validación: no se pueden programar citas en fechas pasadas
        if fecha < timezone.now().date():
            raise ValidationError("No se puede programar citas en fechas pasadas.")

        # Validación: no debe haber citas en el mismo horario
        if Agenda.objects.filter(fecha=fecha, hora=hora).exists():
            raise ValidationError("Ya existe una cita para esa fecha y hora.")

        # Crear y guardar la nueva cita
        cita = Agenda(cliente=cliente, servicio=servicio, fecha=fecha, hora=hora)
        cita.save()
        return cita

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Agenda"

class Registro(models.Model):
    """
    Modelo para llevar un registro histórico de servicios realizados.

    Mantiene un historial completo de todos los servicios prestados.
    """
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE)
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Registro de servicio {self.servicio} para {self.cliente} hecho por {self.empleado} el {self.fecha}"

    def crearRegistro(self, cliente, empleado, servicio, fecha=None):
        """
        Método personalizado para crear registros con validaciones.

        Asegura que no se puedan crear registros con fechas futuras.
        """
        if fecha is None:
            fecha = timezone.now().date()

        # Validación: no se pueden crear registros con fechas futuras
        if fecha > timezone.now().date():
            raise ValidationError("La fecha del registro no puede ser futura.")

        # Crear y guardar el registro
        registro = Registro(cliente=cliente, empleado=empleado, servicio=servicio, fecha=fecha)
        registro.save()
        return registro

    class Meta:
        verbose_name = "Registro"
        verbose_name_plural = "Registros"

class Tarea(models.Model):
    """
    Modelo para gestionar tareas del personal del taller.
    """
    ESTADOS_TAREA = [
        ('por_hacer', 'Por Hacer'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
    ]

    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_TAREA, default='por_hacer')
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_limite = models.DateField(null=True, blank=True)
    
    # Relaciones
    reparacion = models.ForeignKey('Reparacion', on_delete=models.CASCADE, related_name='tareas', null=True, blank=True)
    creada_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas_creadas')
    actualizada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas_actualizadas')
    asignada_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas_asignadas')
    
    etiqueta = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.titulo
        
    def save(self, *args, **kwargs):
        # Actualizar la fecha de actualización al guardar
        self.fecha_actualizacion = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['-fecha_creacion']


class TareaHistorial(models.Model):
    """
    Modelo para registrar el historial de cambios en las tareas.
    """
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tareas_historial')
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(max_length=50)  # creada, actualizada, completada, etc.
    descripcion = models.TextField()
    
    class Meta:
        verbose_name = 'Historial de Tarea'
        verbose_name_plural = 'Historial de Tareas'
        ordering = ['-fecha_cambio']
    
    def __str__(self):
        return f"{self.tarea.titulo} - {self.accion} por {self.usuario.username if self.usuario else 'Sistema'}"

# ========== SIGNALS Y AUTOMATIZACIÓN ==========

# Signal para crear Perfil automáticamente cuando se crea un usuario
# Esto asegura que cada nuevo usuario tenga un Perfil asociado automáticamente
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """
    Signal que se ejecuta automáticamente cuando se crea un nuevo usuario.

    Crea un Perfil básico para cada usuario nuevo con valores por defecto.
    """
    if created:
        UserProfile.objects.create(
            user=instance,
            telefono='',
            es_empleado=False
        )
