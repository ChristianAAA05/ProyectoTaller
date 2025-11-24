"""
Comando para listar todos los usuarios y sus roles.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gestion.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Lista todos los usuarios y sus roles asignados'

    def handle(self, *args, **options):
        users = User.objects.all()
        
        self.stdout.write(self.style.SUCCESS('\n=== USUARIOS Y ROLES ===\n'))
        
        for user in users:
            try:
                profile = user.profile
                roles = []
                if profile.es_jefe:
                    roles.append('JEFE')
                if profile.es_encargado:
                    roles.append('ENCARGADO')
                if profile.es_mecanico:
                    roles.append('MECÁNICO')
                if profile.es_empleado:
                    roles.append('EMPLEADO')
                if not roles:
                    roles.append('CLIENTE')
                    
                roles_str = ', '.join(roles)
                self.stdout.write(f'  • {user.username} ({user.email}) - Roles: {roles_str}')
            except UserProfile.DoesNotExist:
                self.stdout.write(f'  • {user.username} ({user.email}) - SIN PERFIL')
        
        self.stdout.write('\n')
