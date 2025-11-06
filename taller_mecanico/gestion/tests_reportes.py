from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from gestion.models import Cliente, Servicio, Vehiculo, Reparacion

class ReportesIngresosTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='jefe', password='secret')
        self.client.login(username='jefe', password='secret')
        c = Cliente.objects.create(nombre='A', apellido='B', telefono='1', direccion='X', correo_electronico='a@b.com')
        s = Servicio.objects.create(nombre_servicio='Aceite', descripcion='Cambio', costo=50, duracion=30)
        v = Vehiculo.objects.create(cliente=c, marca='Fiat', modelo='Uno', año=2010, placa='ABC123')
        Reparacion.objects.create(vehiculo=v, servicio=s, estado_reparacion='completada')

    def test_link_in_dashboard_jefe(self):
        resp = self.client.get(reverse('dashboard_jefe'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, reverse('reportes_ingresos'))

    def test_reportes_ingresos_page(self):
        resp = self.client.get(reverse('reportes_ingresos'))
        self.assertEqual(resp.status_code, 200)
        # Should render chart labels data
        self.assertContains(resp, 'Reporte de Ingresos')
