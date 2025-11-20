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
        parser.add_argument('--apellido', type=str, default='', help='Apellido del empleado')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']
        puesto = options['puesto']
        nombre = options['nombre'] or username
        apellido = options['apellido'] or ''

        try:
            # Crear el usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=nombre,
                last_name=apellido
            )
            
            # Crear el perfil de usuario
            profile = UserProfile.objects.create(
                user=user,
                es_empleado=True
            )
            
            # Crear el empleado relacionado
            empleado = Empleado.objects.create(
                user_profile=profile,
                nombres=nombre,
                apellidos=apellido,
                puesto=puesto,
                telefono='',  # Puedes modificar esto según sea necesario
                direccion='',  # Puedes modificar esto según sea necesario
                fecha_ingreso='2000-01-01'  # Fecha por defecto, modifica según sea necesario
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Usuario "{username}" creado exitosamente con perfil de {puesto}.')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Puedes iniciar sesión con usuario: {username} y la contraseña proporcionada.')
            )
            
        except Exception as e:
            raise CommandError(f'Error al crear el usuario: {str(e)}')
