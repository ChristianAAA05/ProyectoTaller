from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from gestion.models import UserProfile, Empleado

class Command(BaseCommand):
    help = 'Crea un nuevo usuario con perfil de empleado y rol específico'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nombre de usuario')
        parser.add_argument('password', type=str, help='Contraseña')
        parser.add_argument('--email', type=str, default='', help='Correo electrónico')
        parser.add_argument('--puesto', type=str, default='mecanico',
                          choices=['mecanico', 'jefe', 'encargado', 'administrativo'],
                          help='Puesto del empleado')
        parser.add_argument('--nombre', type=str, default='', help='Nombre del empleado')
        parser.add_argument('--telefono', type=str, default='', help='Teléfono del empleado')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email'] or f'{username}@taller.local'
        puesto = options['puesto']
        nombre = options['nombre'] or username.capitalize()
        telefono = options['telefono']

        try:
            # Verificar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                raise CommandError(f'El usuario "{username}" ya existe.')

            # Verificar si el email ya existe en Empleado
            if email and Empleado.objects.filter(correo_electronico=email).exists():
                raise CommandError(f'Ya existe un empleado con el correo "{email}".')

            # Crear el usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=nombre
            )

            # Crear el empleado relacionado
            empleado = Empleado.objects.create(
                nombre=nombre,
                puesto=puesto.capitalize(),
                telefono=telefono,
                correo_electronico=email
            )

            # Crear o actualizar el perfil de usuario
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'es_empleado': True,
                    'empleado_relacionado': empleado
                }
            )

            if not created:
                profile.es_empleado = True
                profile.empleado_relacionado = empleado
                profile.save()

            self.stdout.write(
                self.style.SUCCESS(f'Usuario "{username}" creado exitosamente con perfil de {puesto}.')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Empleado: {nombre} ({email})')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Puedes iniciar sesión con usuario: {username} y la contraseña proporcionada.')
            )

        except Exception as e:
            raise CommandError(f'Error al crear el usuario: {str(e)}')
