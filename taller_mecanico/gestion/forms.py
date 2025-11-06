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
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Cliente, Empleado, Servicio, Vehiculo, Reparacion, Agenda

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
            'puesto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Mecánico, Recepcionista, Jefe de Taller',
                'list': 'puestos-sugeridos'
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


class ReparacionForm(forms.ModelForm):
    """
    Formulario para crear y editar reparaciones en el taller.
    
    Permite gestionar la información de las reparaciones de vehículos,
    incluyendo el vehículo, servicio, fechas y estado.
    """
    # Definir las opciones para los campos de selección
    CONDICION_OPCIONES = [
        ('excelente', 'Excelente - Vehículo como nuevo, solo mantenimiento preventivo'),
        ('bueno', 'Bueno - Desgaste leve, puede necesitar ajustes menores'),
        ('regular', 'Regular - Desgaste notable, necesita reparaciones moderadas'),
        ('malo', 'Malo - Desgastado, necesita reparaciones extensas'),
        ('critico', 'Crítico - Daño estructural, posible pérdida total'),
    ]
    
    ESTADO_REPARACION = [
        ('pendiente', '🟡 Pendiente'),
        ('en_progreso', '🔵 En Progreso'),
        ('en_espera', '🟠 En Espera de Repuestos'),
        ('revision', '🟣 Lista para Revisión'),
        ('completada', '🟢 Completada'),
        ('cancelada', '🔴 Cancelada'),
    ]
    
    # Sobrescribir los campos para usar las opciones definidas
    condicion_vehiculo = forms.ChoiceField(
        choices=CONDICION_OPCIONES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True,
            'title': 'Seleccione la condición del vehículo'
        })
    )
    
    estado_reparacion = forms.ChoiceField(
        choices=ESTADO_REPARACION,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True,
            'title': 'Seleccione el estado de la reparación'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Establecer valores iniciales si no se proporcionan
        if not self.instance.pk:  # Solo para formularios nuevos
            self.initial['condicion_vehiculo'] = 'regular'
            self.initial['estado_reparacion'] = 'pendiente'
        
        # Personalizar el campo de notas
        self.fields['notas'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ingrese notas adicionales sobre la reparación...'
        })

    class Meta:
        model = Reparacion
        fields = ['vehiculo', 'servicio', 'fecha_salida', 'condicion_vehiculo', 'estado_reparacion', 'notas']
        
        # Labels personalizados
        labels = {
            'vehiculo': 'Vehículo',
            'servicio': 'Servicio',
            'fecha_salida': 'Fecha de Salida (opcional)',
            'condicion_vehiculo': 'Condición del Vehículo',
            'estado_reparacion': 'Estado de la Reparación',
            'notas': 'Notas Adicionales'
        }
        
        # Widgets personalizados
        widgets = {
            'vehiculo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'servicio': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha_salida': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            })
        }
        
        help_texts = {
            'condicion_vehiculo': 'Seleccione la condición actual del vehículo.',
            'estado_reparacion': 'Seleccione el estado actual de la reparación.',
            'notas': 'Puede agregar notas adicionales sobre la reparación.'
        }


class CitaForm(forms.ModelForm):
    """Formulario para crear y editar citas en el taller.
    
    Permite gestionar las citas de los clientes, incluyendo el servicio,
    fecha y hora de la cita.
    """
    class Meta:
        model = Agenda
        fields = ['cliente', 'servicio', 'fecha', 'hora']
        
        # Widgets personalizados
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'title': 'Seleccione el cliente'
            }),
            'servicio': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'title': 'Seleccione el servicio'
            }),
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': timezone.now().strftime('%Y-%m-%d'),
                'required': True
            }),
            'hora': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'id': 'hora-select'
            })
        }
    
    def clean_fecha(self):
        """Valida que la fecha no sea pasada"""
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha < timezone.now().date():
            raise ValidationError('No se pueden agendar citas en fechas pasadas.')
        return fecha
    
    def clean(self):
        """Valida que no exista otra cita en la misma fecha y hora"""
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        
        if fecha and hora:
            # Si estamos editando una cita, excluirla de la validación
            if self.instance and self.instance.pk:
                if Agenda.objects.filter(fecha=fecha, hora=hora).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe una cita programada para esta fecha y hora.')
            # Si es una cita nueva
            elif Agenda.objects.filter(fecha=fecha, hora=hora).exists():
                raise ValidationError('Ya existe una cita programada para esta fecha y hora.')
        
        return cleaned_data
