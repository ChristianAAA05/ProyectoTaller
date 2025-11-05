from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

from gestion.models import Cliente, Empleado, Servicio, Vehiculo, Reparacion, Agenda, Registro


class DashboardJefeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='jefe', password='secret')
        self.client.login(username='jefe', password='secret')

        # Datos base
        self.cliente = Cliente.objects.create(
            nombre='Ana', apellido='Gomez', telefono='555', direccion='Calle 123', correo_electronico='ana@example.com'
        )
        self.empleado = Empleado.objects.create(
            nombre='Carlos', puesto='Mecánico', telefono='555-111', correo_electronico='carlos@example.com'
        )
        self.servicio = Servicio.objects.create(
            nombre_servicio='Frenos', descripcion='Cambio de pastillas', costo=120, duracion=90
        )
        self.vehiculo = Vehiculo.objects.create(
            cliente=self.cliente, marca='Ford', modelo='Focus', año=2016, placa='XYZ789'
        )

        # Reparaciones en distintos estados
        Reparacion.objects.create(vehiculo=self.vehiculo, servicio=self.servicio, estado_reparacion='pendiente')
        Reparacion.objects.create(vehiculo=self.vehiculo, servicio=self.servicio, estado_reparacion='en_progreso')
        Reparacion.objects.create(vehiculo=self.vehiculo, servicio=self.servicio, estado_reparacion='en_espera')
        Reparacion.objects.create(vehiculo=self.vehiculo, servicio=self.servicio, estado_reparacion='revision')
        Reparacion.objects.create(vehiculo=self.vehiculo, servicio=self.servicio, estado_reparacion='cancelada')
        Reparacion.objects.create(vehiculo=self.vehiculo, servicio=self.servicio, estado_reparacion='completada')

        # Registro para empleados destacados (últimos 30 días)
        Registro.objects.create(cliente=self.cliente, empleado=self.empleado, servicio=self.servicio)

        # Cita próxima
        self.maniana = timezone.now().date() + timedelta(days=1)
        Agenda.objects.create(cliente=self.cliente, servicio=self.servicio, fecha=self.maniana, hora=timezone.now().time().replace(hour=10, minute=0, second=0, microsecond=0))

    def test_dashboard_jefe_links_present(self):
        resp = self.client.get(reverse('dashboard_jefe'))
        self.assertEqual(resp.status_code, 200)
        # Enlaces esenciales
        self.assertContains(resp, reverse('vehiculos-lista'))
        self.assertContains(resp, reverse('vehiculo-agregar'))
        self.assertContains(resp, reverse('dashboard_reparaciones'))
        self.assertContains(resp, reverse('crear_reparacion'))
        self.assertContains(resp, reverse('lista_citas'))
        self.assertContains(resp, reverse('crear_cita'))

    def test_dashboard_jefe_estado_reparaciones_context(self):
        resp = self.client.get(reverse('dashboard_jefe'))
        self.assertEqual(resp.status_code, 200)
        estados = resp.context['reparaciones_por_estado']
        # Convertir a dict {estado: total}
        estados_map = {item['estado']: item['total'] for item in estados}
        expected = {
            'Pendiente': 1,
            'En Proceso': 1,
            'En Espera': 1,
            'Para Revisión': 1,
            'Completada': 1,
            'Cancelada': 1,
        }
        for k, v in expected.items():
            self.assertEqual(estados_map.get(k), v, f"Estado {k} debería ser {v}")

    def test_dashboard_jefe_empleados_destacados(self):
        resp = self.client.get(reverse('dashboard_jefe'))
        self.assertEqual(resp.status_code, 200)
        destacados = resp.context['empleados_destacados']
        self.assertTrue(any(d['nombre'] == 'Carlos' for d in destacados))

    def test_reparacion_crud(self):
        # Crear
        crear_url = reverse('crear_reparacion')
        data = {
            'vehiculo': self.vehiculo.id,
            'servicio': self.servicio.id,
            'condicion_vehiculo': 'bueno',
            'estado_reparacion': 'pendiente',
            'notas': 'Prueba'
        }
        resp = self.client.post(crear_url, data)
        self.assertEqual(resp.status_code, 302)
        rep = Reparacion.objects.order_by('-id').first()
        self.assertIsNotNone(rep)
        # Editar
        editar_url = reverse('editar_reparacion', args=[rep.id])
        data_edit = {
            'vehiculo': self.vehiculo.id,
            'servicio': self.servicio.id,
            'condicion_vehiculo': 'regular',
            'estado_reparacion': 'completada',
            'fecha_salida': (timezone.now() + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M'),
            'notas': 'Finalizada'
        }
        resp = self.client.post(editar_url, data_edit)
        self.assertEqual(resp.status_code, 302)
        rep.refresh_from_db()
        self.assertEqual(rep.estado_reparacion, 'completada')
        # Eliminar
        eliminar_url = reverse('eliminar_reparacion', args=[rep.id])
        resp = self.client.post(eliminar_url)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Reparacion.objects.filter(id=rep.id).exists())

    def test_cita_crud(self):
        # Crear cita
        crear_url = reverse('crear_cita')
        hora = '10:00'
        data = {
            'cliente': self.cliente.id,
            'servicio': self.servicio.id,
            'fecha': (timezone.now().date() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'hora': hora,
        }
        resp = self.client.post(crear_url, data)
        self.assertEqual(resp.status_code, 302)
        cita = Agenda.objects.order_by('-id').first()
        self.assertIsNotNone(cita)
        # Editar cita
        editar_url = reverse('editar_cita', args=[cita.id])
        data_edit = {
            'cliente': self.cliente.id,
            'servicio': self.servicio.id,
            'fecha': (timezone.now().date() + timedelta(days=3)).strftime('%Y-%m-%d'),
            'hora': '11:00',
        }
        resp = self.client.post(editar_url, data_edit)
        self.assertEqual(resp.status_code, 302)
        cita.refresh_from_db()
        self.assertEqual(cita.hora.strftime('%H:%M'), '11:00')
        # Eliminar cita
        eliminar_url = reverse('eliminar_cita', args=[cita.id])
        resp = self.client.post(eliminar_url)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Agenda.objects.filter(id=cita.id).exists())

    def test_proximas_citas_en_dashboard(self):
        resp = self.client.get(reverse('dashboard_jefe'))
        self.assertEqual(resp.status_code, 200)
        # Debe traer por lo menos una próxima cita
        self.assertTrue(len(resp.context['citas_proximas']) >= 1)
