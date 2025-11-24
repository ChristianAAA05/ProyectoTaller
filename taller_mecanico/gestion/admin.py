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
    list_display = ('nombre', 'apellido', 'telefono', 'correo_electronico', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'telefono', 'correo_electronico')
    list_filter = ('fecha_registro',)
    readonly_fields = ('fecha_registro',)
    date_hierarchy = 'fecha_registro'

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'puesto', 'telefono', 'correo_electronico')
    search_fields = ('nombre', 'puesto', 'correo_electronico')
    list_filter = ('puesto',)

class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre_servicio', 'descripcion', 'costo', 'duracion')
    search_fields = ('nombre_servicio', 'descripcion')
    list_filter = ('nombre_servicio',)

class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'año', 'placa', 'vin', 'cliente', 'get_cliente_telefono', 'get_cliente_email')
    search_fields = (
        'marca', 'modelo', 'placa', 'vin',
        'cliente__nombre', 'cliente__apellido',
        'cliente__telefono', 'cliente__correo_electronico'
    )
    list_filter = ('marca', 'año', 'cliente')
    list_select_related = ('cliente',)
    autocomplete_fields = ['cliente']
    list_per_page = 20
    save_on_top = True
    
    fieldsets = (
        ('Información del Vehículo', {
            'fields': ('marca', 'modelo', 'año', 'placa')
        }),
        ('Datos Adicionales', {
            'fields': ('vin',),
            'classes': ('collapse',)
        }),
        ('Propietario', {
            'fields': ('cliente',)
        }),
    )
    
    def get_cliente_telefono(self, obj):
        return obj.cliente.telefono
    get_cliente_telefono.short_description = 'Teléfono Cliente'
    get_cliente_telefono.admin_order_field = 'cliente__telefono'
    
    def get_cliente_email(self, obj):
        return obj.cliente.correo_electronico
    get_cliente_email.short_description = 'Email Cliente'
    get_cliente_email.admin_order_field = 'cliente__correo_electronico'

class ReparacionAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'servicio', 'fecha_ingreso', 'fecha_salida', 'estado_reparacion', 'condicion_vehiculo')
    search_fields = ('vehiculo__marca', 'vehiculo__modelo', 'estado_reparacion', 'condicion_vehiculo')
    list_filter = ('estado_reparacion', 'condicion_vehiculo', 'fecha_ingreso')
    list_editable = ('estado_reparacion', 'condicion_vehiculo')
    list_select_related = ('vehiculo', 'servicio')
    date_hierarchy = 'fecha_ingreso'

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
