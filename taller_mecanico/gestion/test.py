from django.test import TestCase
from django.template.loader import select_template

class TemplateSearchTest(TestCase):
    def test_encontrar_template(self):
        # Intenta cargar el template por varias rutas posibles
        templates_to_test = [
            'clientes_lista.html',
            'gestion/clientes_lista.html',
            'templates/gestion/clientes_lista.html',
        ]
        for template_name in templates_to_test:
            with self.subTest(template=template_name):
                try:
                    template = select_template([template_name])
                    self.assertIsNotNone(template)
                    print(f"Template encontrado: {template_name}")
                    return
                except Exception as e:
                    print(f"No se encontró template: {template_name} - {e}")
        self.fail("No se pudo encontrar ninguna de las plantillas especificadas.")
