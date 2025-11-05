from django.test import TestCase
from django.utils import timezone
from datetime import date, time, timedelta
from gestion.models import Cliente, Empleado, Servicio, Agenda, Registro
from django.core.exceptions import ValidationError

class AgendaRegistroTestCase(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre="Cliente Test",
            apellido="Prueba",
            telefono="12345678",
            direccion="Calle Falsa 123",
            correo_electronico="cliente_test@example.com"
        )
        self.empleado = Empleado.objects.create(
            nombre="Empleado Test",
            puesto="Mecánico",
            telefono="87654321",
            correo_electronico="empleado_test@example.com"
        )
        self.servicio = Servicio.objects.create(nombre_servicio="Cambio de aceite", duracion=30, costo=50)

    def test_programar_cita_exitosa(self):
        fecha = timezone.now().date() + timedelta(days=1)
        hora = time(10, 0)
        cita = Agenda()
        cita = cita.programarCita(self.cliente, self.servicio, fecha, hora)
        self.assertEqual(cita.cliente, self.cliente)
        self.assertEqual(cita.servicio, self.servicio)
        self.assertEqual(cita.fecha, fecha)
        self.assertEqual(cita.hora, hora)

    def test_programar_cita_fecha_pasada(self):
        cita = Agenda()
        fecha_pasada = timezone.now().date() - timedelta(days=1)
        hora = time(10, 0)
        with self.assertRaises(ValidationError):
            cita.programarCita(self.cliente, self.servicio, fecha_pasada, hora)

    def test_programar_cita_horario_ocupado(self):
        fecha = timezone.now().date() + timedelta(days=1)
        hora = time(10, 0)
        # Crear cita previa para el mismo horario
        Agenda.objects.create(cliente=self.cliente, servicio=self.servicio, fecha=fecha, hora=hora)
        cita = Agenda()
        with self.assertRaises(ValidationError):
            cita.programarCita(self.cliente, self.servicio, fecha, hora)

    def test_crear_registro_exitosa(self):
        fecha = timezone.now().date()
        registro = Registro()
        registro = registro.crearRegistro(self.cliente, self.empleado, self.servicio, fecha)
        self.assertEqual(registro.cliente, self.cliente)
        self.assertEqual(registro.empleado, self.empleado)
        self.assertEqual(registro.servicio, self.servicio)
        self.assertEqual(registro.fecha, fecha)

    def test_crear_registro_fecha_futura(self):
        registro = Registro()
        fecha_futura = timezone.now().date() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            registro.crearRegistro(self.cliente, self.empleado, self.servicio, fecha_futura)
