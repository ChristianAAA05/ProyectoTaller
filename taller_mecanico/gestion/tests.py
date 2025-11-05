from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

from gestion.models import Cliente, Empleado, Servicio, Vehiculo


class BasicViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='secret')
        self.client.login(username='tester', password='secret')

        self.cliente = Cliente.objects.create(
            nombre='Juan', apellido='Perez', telefono='123456', direccion='Calle 1', correo_electronico='juan@example.com'
        )
        self.empleado = Empleado.objects.create(
            nombre='Mario', puesto='Mecánico', telefono='111222', correo_electronico='mario@example.com'
        )
        self.servicio = Servicio.objects.create(
            nombre_servicio='Cambio de aceite', descripcion='Desc', costo=50, duracion=30
        )
        self.vehiculo = Vehiculo.objects.create(
            cliente=self.cliente, marca='Toyota', modelo='Corolla', año=2018, placa='ABC123'
        )

    def test_list_pages_load(self):
        urls = [
            'clientes-lista',
            'empleados-lista',
            'servicios-lista',
            'vehiculos-lista',
        ]
        for name in urls:
            with self.subTest(url=name):
                resp = self.client.get(reverse(name))
                self.assertEqual(resp.status_code, 200)

    def test_create_servicio(self):
        resp = self.client.post(reverse('servicios-crear'), {
            'nombre_servicio': 'Alineación',
            'descripcion': 'Serv',
            'costo': '100.50',
            'duracion': 60,
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Servicio.objects.filter(nombre_servicio='Alineación').exists())

    def test_api_horas_disponibles(self):
        fecha = (timezone.now().date() + timedelta(days=1)).strftime('%Y-%m-%d')
        url = reverse('obtener_horas_disponibles', kwargs={'fecha': fecha})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('horas_disponibles', data)
        self.assertIsInstance(data['horas_disponibles'], list)

    def test_buscar_clientes(self):
        resp = self.client.get(reverse('buscar-clientes'), {'q': 'Juan'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # Acepta cualquiera de los formatos soportados
        lista = data.get('results') or data.get('clientes')
        self.assertIsInstance(lista, list)
        self.assertTrue(any(item['id'] == self.cliente.id for item in lista))
