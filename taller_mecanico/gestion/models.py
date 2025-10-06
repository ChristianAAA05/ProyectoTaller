from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

fecha = models.DateField(null=True, blank=True)

# Create your models here.

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)
    correo_electronico = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    puesto = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    nombre_servicio = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    duracion = models.IntegerField() # Duración en minutos

    def __str__(self):
        return self.nombre_servicio

class Vehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vehiculos')
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    año = models.IntegerField()
    placa = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"

class Reparacion(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='reparaciones')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=50, default='En progreso') # E.g., 'En progreso', 'Completado', 'Pendiente'
    
    def __str__(self):
        return f"Reparación de {self.vehiculo} - {self.servicio}"

class Agenda(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"Cita para {self.cliente} - {self.servicio} el {self.fecha} a las {self.hora}"

    def programarCita(self, cliente, servicio, fecha, hora):
        # Verifica que la fecha y hora no estén en el pasado
        if fecha < timezone.now().date():
            raise ValidationError("No se puede programar citas en fechas pasadas.")
        # Verifica que no haya una cita para la misma fecha y hora
        if Agenda.objects.filter(fecha=fecha, hora=hora).exists():
            raise ValidationError("Ya existe una cita para esa fecha y hora.")
        # Crear la cita
        cita = Agenda(cliente=cliente, servicio=servicio, fecha=fecha, hora=hora)
        cita.save()
        return cita


class Registro(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE)
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Registro de servicio {self.servicio} para {self.cliente} hecho por {self.empleado} el {self.fecha}"

    def crearRegistro(self, cliente, empleado, servicio, fecha=None):
        if fecha is None:
            fecha = timezone.now().date()
        if fecha > timezone.now().date():
            raise ValidationError("La fecha del registro no puede ser futura.")
        registro = Registro(cliente=cliente, empleado=empleado, servicio=servicio, fecha=fecha)
        registro.save()
        return registro
