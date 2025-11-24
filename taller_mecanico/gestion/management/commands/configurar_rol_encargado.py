"""
Comando para configurar un usuario como encargado del taller.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gestion.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Configura un usuario como encargado del taller'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nombre de usuario a configurar como encargado')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            
            # Crear o actualizar el perfil
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.es_encargado = True
            profile.es_empleado = True
            profile.save()
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Perfil creado y configurado para {username} como ENCARGADO'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Usuario {username} configurado como ENCARGADO'))
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Usuario {username} no encontrado'))
