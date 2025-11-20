import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taller_mecanico.settings')
django.setup()

from django.contrib.auth.models import User
from gestion.models import UserProfile, Empleado

def verificar_usuario(username):
    try:
        user = User.objects.get(username=username)
        print(f"\n--- Verificando usuario: {username} ---")
        
        # Verificar si el usuario tiene perfil
        if hasattr(user, 'profile'):
            print("✅ El usuario tiene perfil")
            print(f"   - Es empleado: {user.profile.es_empleado}")
            
            # Verificar si el perfil tiene empleado relacionado
            if hasattr(user.profile, 'empleado_relacionado'):
                empleado = user.profile.empleado_relacionado
                print(f"✅ Tiene empleado relacionado")
                print(f"   - Puesto: {empleado.puesto}")
                print(f"   - Nombre: {empleado.nombres} {empleado.apellidos}")
            else:
                print("❌ No tiene empleado relacionado")
                # Crear empleado relacionado
                crear_empleado = input("¿Deseas crear un empleado relacionado? (s/n): ")
                if crear_empleado.lower() == 's':
                    crear_empleado_para_usuario(user)
        else:
            print("❌ El usuario no tiene perfil")
            crear_perfil = input("¿Deseas crear un perfil para este usuario? (s/n): ")
            if crear_perfil.lower() == 's':
                crear_perfil_para_usuario(user)
    
    except User.DoesNotExist:
        print(f"❌ El usuario {username} no existe")

def crear_perfil_para_usuario(user):
    """Crea un perfil de usuario con es_empleado=True"""
    try:
        profile = UserProfile.objects.create(
            user=user,
            es_empleado=True
        )
        print(f"✅ Perfil creado exitosamente para {user.username}")
        
        # Preguntar si se desea crear empleado relacionado
        crear_empleado = input("¿Deseas crear un empleado relacionado? (s/n): ")
        if crear_empleado.lower() == 's':
            crear_empleado_para_usuario(user)
    
    except Exception as e:
        print(f"❌ Error al crear el perfil: {str(e)}")

def crear_empleado_para_usuario(user):
    """Crea un empleado relacionado con el perfil del usuario"""
    try:
        if not hasattr(user, 'profile'):
            print("❌ El usuario no tiene perfil. Creando perfil primero...")
            user.profile = UserProfile.objects.create(user=user, es_empleado=True)
        
        # Obtener datos del empleado
        print("\n--- Creando empleado ---")
        nombres = input("Nombres (dejar en blanco para usar nombre de usuario): ") or user.username
        apellidos = input("Apellidos: ") or ""
        
        # Mostrar opciones de puesto
        print("\nOpciones de puesto:")
        print("1. Mecánico")
        print("2. Jefe")
        print("3. Encargado")
        print("4. Administrativo")
        opcion = input("Seleccione el número correspondiente al puesto: ")
        
        puestos = {
            '1': 'mecanico',
            '2': 'jefe',
            '3': 'encargado',
            '4': 'administrativo'
        }
        
        puesto = puestos.get(opcion, 'mecanico')
        
        # Crear empleado
        empleado = Empleado.objects.create(
            user_profile=user.profile,
            nombres=nombres,
            apellidos=apellidos,
            puesto=puesto,
            telefono='',
            direccion='',
            fecha_ingreso='2023-01-01'  # Fecha por defecto
        )
        
        print(f"✅ Empleado creado exitosamente con puesto: {puesto}")
        
    except Exception as e:
        print(f"❌ Error al crear el empleado: {str(e)}")

if __name__ == "__main__":
    username = input("Ingrese el nombre de usuario a verificar: ")
    verificar_usuario(username)
