from django.db import models
from django.utils import timezone

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
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    servicio_solicitado = models.CharField(max_length=200)
    confirmada = models.BooleanField(default=False)

    def __str__(self):
        return f"Cita de {self.cliente} para {self.vehiculo} el {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"

class Registro(models.Model):
    reparacion = models.ForeignKey(Reparacion, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Registro para {self.reparacion} el {self.fecha.strftime('%Y-%m-%d')}"
