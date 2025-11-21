"""
Comando para crear usuarios de prueba para el sistema del taller mecánico.

Este comando crea automáticamente los usuarios de prueba que se mencionan
en la página de login, facilitando las pruebas y demostraciones del sistema.

Usuarios creados:
- jefe / jefe123 (Jefe del taller - acceso completo)
- encargado / encargado123 (Encargado - gestión operacional)
- mecanico / mecanico123 (Mecánico - vista de reparaciones asignadas)
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import transaction
from gestion.models import UserProfile, Empleado


class Command(BaseCommand):
    help = 'Crea usuarios de prueba para el sistema del taller mecánico'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina y recrea los usuarios de prueba si ya existen',
        )

    def handle(self, *args, **options):
        reset = options.get('reset', False)

        # Definir usuarios de prueba
        test_users = [
            {
                'username': 'jefe',
                'password': 'jefe123',
                'email': 'jefe@taller.local',
                'first_name': 'Roberto',
                'puesto': 'Jefe',
                'telefono': '0981-123-456',
            },
            {
                'username': 'encargado',
                'password': 'encargado123',
                'email': 'encargado@taller.local',
                'first_name': 'Carlos',
                'puesto': 'Encargado',
                'telefono': '0981-234-567',
            },
            {
                'username': 'mecanico',
                'password': 'mecanico123',
                'email': 'mecanico@taller.local',
                'first_name': 'Juan',
                'puesto': 'Mecanico',
                'telefono': '0981-345-678',
            },
        ]

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for user_data in test_users:
            username = user_data['username']

            try:
                with transaction.atomic():
                    # Verificar si el usuario ya existe
                    if User.objects.filter(username=username).exists():
                        if reset:
                            # Eliminar usuario existente y recrear
                            self.stdout.write(
                                self.style.WARNING(f'Eliminando usuario existente: {username}')
                            )
                            user = User.objects.get(username=username)

                            # Eliminar empleado relacionado si existe
                            try:
                                empleado = Empleado.objects.get(correo_electronico=user_data['email'])
                                empleado.delete()
                            except Empleado.DoesNotExist:
                                pass

                            # Eliminar perfil (se elimina automáticamente con CASCADE)
                            user.delete()
                        else:
                            self.stdout.write(
                                self.style.WARNING(f'Usuario "{username}" ya existe. Use --reset para recrear.')
                            )
                            skipped_count += 1
                            continue

                    # Crear el usuario
                    user = User.objects.create_user(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=user_data['password'],
                        first_name=user_data['first_name']
                    )

                    # Crear el empleado
                    empleado = Empleado.objects.create(
                        nombre=user_data['first_name'],
                        puesto=user_data['puesto'],
                        telefono=user_data['telefono'],
                        correo_electronico=user_data['email']
                    )

                    # Crear el perfil de usuario (se crea automáticamente por signal)
                    # pero lo actualizamos para asegurar la relación con empleado
                    profile = UserProfile.objects.get(user=user)
                    profile.es_empleado = True
                    profile.empleado_relacionado = empleado
                    profile.save()

                    if reset and skipped_count > 0:
                        updated_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Usuario "{username}" recreado exitosamente')
                        )
                    else:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Usuario "{username}" creado exitosamente')
                        )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error al procesar usuario "{username}": {str(e)}')
                )
                continue

        # Mostrar resumen
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('RESUMEN DE CREACIÓN DE USUARIOS DE PRUEBA'))
        self.stdout.write('='*60)

        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Usuarios creados: {created_count}')
            )

        if updated_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'↻ Usuarios recreados: {updated_count}')
            )

        if skipped_count > 0:
            self.stdout.write(
                self.style.WARNING(f'⊘ Usuarios omitidos (ya existían): {skipped_count}')
            )

        self.stdout.write('\n' + 'Credenciales de acceso:')
        self.stdout.write('-'*60)
        for user_data in test_users:
            self.stdout.write(
                f"  {user_data['puesto']:12} → {user_data['username']:12} / {user_data['password']}"
            )

        self.stdout.write('\n' + self.style.SUCCESS('✓ Proceso completado'))
        self.stdout.write(
            'Puedes iniciar sesión en http://127.0.0.1:8000/login/\n'
        )
