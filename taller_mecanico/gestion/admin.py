from django.contrib import admin
from .models import Cliente, Empleado, Servicio, Vehiculo, Reparacion, Agenda, Registro

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Servicio)
admin.site.register(Vehiculo)
admin.site.register(Reparacion)
admin.site.register(Agenda)
admin.site.register(Registro)
