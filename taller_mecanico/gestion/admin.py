from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Cliente, Empleado, Servicio, Vehiculo, Reparacion, Agenda, Registro, UserProfile

# Configuración personalizada para UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil de usuario'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# Configuración para modelos del taller
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'correo_electronico', 'direccion')
    search_fields = ('nombre', 'correo_electronico')
    list_filter = ('nombre',)

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'puesto', 'telefono', 'correo_electronico')
    search_fields = ('nombre', 'puesto', 'correo_electronico')
    list_filter = ('puesto',)

class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre_servicio', 'descripcion', 'costo', 'duracion')
    search_fields = ('nombre_servicio', 'descripcion')
    list_filter = ('nombre_servicio',)

class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'año', 'placa', 'cliente')
    search_fields = ('marca', 'modelo', 'placa')
    list_filter = ('marca', 'año')

class ReparacionAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'servicio', 'fecha_ingreso', 'fecha_salida', 'estado')
    search_fields = ('vehiculo__marca', 'vehiculo__modelo', 'estado')
    list_filter = ('estado', 'fecha_ingreso')

class AgendaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'servicio', 'fecha', 'hora')
    search_fields = ('cliente__nombre', 'servicio__nombre_servicio')
    list_filter = ('fecha', 'servicio')
    date_hierarchy = 'fecha'

class RegistroAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'empleado', 'servicio', 'fecha')
    search_fields = ('cliente__nombre', 'empleado__nombre', 'servicio__nombre_servicio')
    list_filter = ('fecha', 'servicio')

# Registrar modelos con configuraciones personalizadas
admin.site.unregister(User)  # Desregistrar el UserAdmin por defecto
admin.site.register(User, CustomUserAdmin)  # Registrar con nuestra configuración personalizada
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Vehiculo, VehiculoAdmin)
admin.site.register(Reparacion, ReparacionAdmin)
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(Registro, RegistroAdmin)
admin.site.register(UserProfile)
