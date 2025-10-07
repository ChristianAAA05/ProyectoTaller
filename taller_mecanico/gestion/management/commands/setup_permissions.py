from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from gestion.models import Cliente, Empleado, Servicio, Vehiculo, Reparacion, Agenda, Registro

class Command(BaseCommand):
    help = 'Crear grupos de permisos para el taller mecánico'

    def handle(self, *args, **options):
        # Crear grupos
        admin_group, created = Group.objects.get_or_create(name='Administradores')
        mecanico_group, created = Group.objects.get_or_create(name='Mecánicos')
        recepcion_group, created = Group.objects.get_or_create(name='Recepción')
        contable_group, created = Group.objects.get_or_create(name='Contabilidad')

        # Obtener content types
        cliente_ct = ContentType.objects.get_for_model(Cliente)
        empleado_ct = ContentType.objects.get_for_model(Empleado)
        servicio_ct = ContentType.objects.get_for_model(Servicio)
        vehiculo_ct = ContentType.objects.get_for_model(Vehiculo)
        reparacion_ct = ContentType.objects.get_for_model(Reparacion)
        agenda_ct = ContentType.objects.get_for_model(Agenda)
        registro_ct = ContentType.objects.get_for_model(Registro)

        # Permisos para Administradores (acceso completo)
        admin_permissions = Permission.objects.filter(
            content_type__in=[
                cliente_ct, empleado_ct, servicio_ct, vehiculo_ct,
                reparacion_ct, agenda_ct, registro_ct
            ]
        )
        admin_group.permissions.set(admin_permissions)

        # Permisos para Mecánicos (solo ver y editar reparaciones)
        mecanico_permissions = Permission.objects.filter(
            content_type=reparacion_ct,
            codename__in=['view_reparacion', 'change_reparacion']
        )
        mecanico_group.permissions.set(mecanico_permissions)

        # Permisos para Recepción (gestionar clientes, vehículos y citas)
        recepcion_permissions = Permission.objects.filter(
            content_type__in=[cliente_ct, vehiculo_ct, agenda_ct],
        )
        recepcion_group.permissions.set(recepcion_permissions)

        # Permisos para Contabilidad (ver registros y algunos datos financieros)
        contable_permissions = Permission.objects.filter(
            content_type__in=[registro_ct, servicio_ct],
            codename__in=['view_registro', 'view_servicio']
        )
        contable_group.permissions.set(contable_permissions)

        self.stdout.write(
            self.style.SUCCESS('Grupos de permisos creados exitosamente')
        )
