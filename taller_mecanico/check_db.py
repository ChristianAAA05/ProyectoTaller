#!/usr/bin/env python3

import sys
import os
sys.path.append('/home/christian/proyecto Py/ProyectoTaller/taller_mecanico')

# Try to import Django settings
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taller_mecanico.settings')
    import django
    django.setup()

    from gestion.models import Empleado

    # Check if employees exist
    empleados = Empleado.objects.all()
    print(f"Found {empleados.count()} employees in database:")
    for empleado in empleados:
        print(f"- {empleado.nombre} ({empleado.puesto})")

    if empleados.count() == 0:
        print("No employees found in database.")
        print("You might need to run migrations or add some test data.")

except ImportError as e:
    print(f"Django import error: {e}")
    print("Django might not be installed properly.")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
