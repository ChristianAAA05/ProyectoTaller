"""
Formularios de la aplicación Taller Mecánico

Este archivo define los formularios basados en modelos (ModelForm) utilizados
para crear y editar las entidades principales del sistema:

- ClienteForm: Para gestionar información de clientes
- EmpleadoForm: Para gestionar información de empleados
- ServicioForm: Para gestionar el catálogo de servicios
- VehiculoForm: Para gestionar vehículos de clientes

Cada formulario incluye:
- Validación automática de Django
- Campos con atributos CSS para Bootstrap
- Placeholders informativos
- Labels descriptivos
- Widgets personalizados según el tipo de dato
"""

from django import forms
from .models import Cliente, Empleado, Servicio, Vehiculo

class ClienteForm(forms.ModelForm):
    """
    Formulario para crear y editar clientes del taller.

    Utiliza ModelForm para aprovechar la validación automática de Django
    y mantener consistencia con el modelo Cliente.
    """
    class Meta:
        model = Cliente  # Modelo base para el formulario
        fields = ['nombre', 'apellido', 'telefono', 'direccion', 'correo_electronico']  # Campos incluidos

        # Labels personalizados para mejorar la UX
        labels = {
            'nombre': 'Nombre del Cliente',
            'apellido': 'Apellido del Cliente',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'correo_electronico': 'Correo Electrónico'
        }

        # Widgets con atributos CSS para Bootstrap y placeholders informativos
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',  # Clase Bootstrap para estilos
                'placeholder': 'Ingrese el nombre del cliente'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido del cliente'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el teléfono del cliente'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,  # Área de texto de 3 líneas
                'placeholder': 'Ingrese la dirección del cliente'
            }),
            'correo_electronico': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el correo electrónico del cliente'
            })
        }

class EmpleadoForm(forms.ModelForm):
    """
    Formulario para crear y editar empleados del taller.

    Permite gestionar la información del personal con diferentes puestos de trabajo.
    """
    class Meta:
        model = Empleado  # Modelo base para el formulario
        fields = ['nombre', 'puesto', 'telefono', 'correo_electronico']  # Campos incluidos

        # Labels descriptivos para cada campo
        labels = {
            'nombre': 'Nombre del Empleado',
            'puesto': 'Puesto de Trabajo',
            'telefono': 'Teléfono',
            'correo_electronico': 'Correo Electrónico'
        }

        # Widgets configurados para cada tipo de campo
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del empleado'
            }),
            'puesto': forms.Select(attrs={
                'class': 'form-control'
                # Nota: Las opciones se generan automáticamente desde el modelo
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el teléfono del empleado'
            }),
            'correo_electronico': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el correo electrónico del empleado'
            })
        }

class ServicioForm(forms.ModelForm):
    """
    Formulario para crear y editar servicios del catálogo.

    Gestiona el catálogo de servicios con precios y duración estimada.
    """
    class Meta:
        model = Servicio  # Modelo base para el formulario
        fields = ['nombre_servicio', 'descripcion', 'costo', 'duracion']  # Campos incluidos

        # Labels descriptivos para cada campo
        labels = {
            'nombre_servicio': 'Nombre del Servicio',
            'descripcion': 'Descripción',
            'costo': 'Costo',
            'duracion': 'Duración (minutos)'
        }

        # Widgets especializados según el tipo de dato
        widgets = {
            'nombre_servicio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del servicio'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,  # Área de texto de 3 líneas para descripción
                'placeholder': 'Ingrese la descripción del servicio'
            }),
            'costo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',  # Permite decimales para centavos
                'min': '0',      # No permite valores negativos
                'placeholder': '0.00'
            }),
            'duracion': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',      # Duración mínima de 1 minuto
                'placeholder': 'Ingrese la duración en minutos'
            })
        }


class VehiculoForm(forms.ModelForm):
    """
    Formulario para crear y editar vehículos de clientes.

    Permite gestionar la información de los vehículos asociados a cada cliente.
    """
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        required=True,
        label='Cliente',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'cliente_select',
            'style': 'display: none;'  # Ocultamos el select ya que usaremos el buscador
        })
    )
    
    class Meta:
        model = Vehiculo
        fields = ['cliente', 'marca', 'modelo', 'año', 'placa']

        # Labels descriptivos para cada campo
        labels = {
            'marca': 'Marca del Vehículo',
            'modelo': 'Modelo del Vehículo',
            'año': 'Año del Vehículo',
            'placa': 'Placa del Vehículo'
        }

        # Widgets configurados para cada tipo de campo
        widgets = {
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Toyota, Ford, Chevrolet, etc.',
                'required': 'required'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Corolla, F-150, Onix, etc.',
                'required': 'required'
            }),
            'año': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1900',
                'max': '2030',
                'placeholder': 'Año de fabricación',
                'required': 'required'
            }),
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la placa del vehículo',
                'style': 'text-transform: uppercase;',
                'required': 'required'
            }),
        }
