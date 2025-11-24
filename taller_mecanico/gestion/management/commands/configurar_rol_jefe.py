"""
Comando para configurar un usuario como jefe del taller.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gestion.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Configura un usuario como jefe del taller'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nombre de usuario a configurar como jefe')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            
            # Crear o actualizar el perfil
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.es_jefe = True
            profile.es_empleado = True
            profile.save()
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Perfil creado y configurado para {username} como JEFE'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Usuario {username} configurado como JEFE'))
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Usuario {username} no encontrado'))
