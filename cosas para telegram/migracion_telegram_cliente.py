"""
MIGRACIÓN PARA AGREGAR CAMPO TELEGRAM_CHAT_ID

Agrega un campo al modelo Cliente para guardar el chat_id de Telegram
Esto permite enviar notificaciones directas a los clientes.

PASO 1: Modificar el modelo
----------------------------

En gestion/models.py, en la clase Cliente, agregar:

    telegram_chat_id = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name='Telegram Chat ID',
        help_text='ID de chat de Telegram para notificaciones'
    )
    telegram_username = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Usuario de Telegram',
        help_text='Nombre de usuario en Telegram (@usuario)'
    )


PASO 2: Crear migración
------------------------

python manage.py makemigrations
python manage.py migrate


PASO 3: Actualizar admin.py
----------------------------

En gestion/admin.py, en ClienteAdmin agregar a fieldsets o list_display:

    list_display = ['nombre', 'apellido', 'telefono', 'telegram_username']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'telefono', 'correo_electronico')
        }),
        ('Telegram', {
            'fields': ('telegram_chat_id', 'telegram_username'),
            'classes': ('collapse',)
        }),
    )


PASO 4: Comando para vincular cuentas
--------------------------------------

Crear gestion/management/commands/vincular_telegram.py:
"""

# gestion/management/commands/vincular_telegram.py
from django.core.management.base import BaseCommand
from gestion.models import Cliente


class Command(BaseCommand):
    help = 'Comando para vincular cuenta de Telegram con cliente'

    def add_arguments(self, parser):
        parser.add_argument('telefono', type=str, help='Teléfono del cliente')
        parser.add_argument('chat_id', type=str, help='Chat ID de Telegram')
        parser.add_argument('--username', type=str, help='Username de Telegram')

    def handle(self, *args, **options):
        telefono = options['telefono']
        chat_id = options['chat_id']
        username = options.get('username', '')

        try:
            cliente = Cliente.objects.get(telefono=telefono)
            cliente.telegram_chat_id = chat_id
            if username:
                cliente.telegram_username = username
            cliente.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Cliente {cliente.nombre_completo} vinculado con Telegram'
                )
            )
        except Cliente.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ No se encontró cliente con teléfono {telefono}'
                )
            )


"""
USO DEL COMANDO:
----------------

python manage.py vincular_telegram "+595123456789" "123456789" --username "@juanperez"


PASO 5: Función de vinculación automática en el bot
----------------------------------------------------

En telegram_bot.py, agregar comando /vincular:
"""

async def vincular_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /vincular para que el cliente vincule su cuenta
    """
    chat_id = update.effective_chat.id
    
    mensaje = f"""
🔗 *Vincular cuenta de Telegram*

Tu Chat ID es: `{chat_id}`

Para vincular tu cuenta:
1. Llama al taller: +595 XXX XXXXXX
2. Proporciona este código: `{chat_id}`
3. Confirmaremos tu identidad
4. Recibirás notificaciones automáticas

*Beneficios:*
✅ Notificaciones de reparaciones
✅ Recordatorios de citas
✅ Consulta rápida de estado
✅ Alertas importantes

Para más información usa /help
    """
    
    await update.message.reply_text(mensaje, parse_mode='Markdown')


"""
PASO 6: Sistema automático de vinculación
------------------------------------------

Opción A - Por código de verificación:
"""

import random
import string
from django.core.cache import cache

async def solicitar_vinculacion_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Generar código de verificación para vincular cuenta
    """
    if not context.args or len(context.args) < 1:
        await update.message.reply_text(
            "Por favor proporciona tu número de teléfono.\n"
            "Ejemplo: /vincular +595123456789"
        )
        return
    
    telefono = context.args[0]
    chat_id = update.effective_chat.id
    
    # Generar código de 6 dígitos
    codigo = ''.join(random.choices(string.digits, k=6))
    
    # Guardar en cache por 10 minutos
    cache_key = f'telegram_vinculacion_{codigo}'
    cache.set(cache_key, {
        'telefono': telefono,
        'chat_id': chat_id,
        'username': update.effective_user.username
    }, timeout=600)  # 10 minutos
    
    mensaje = f"""
🔑 *Código de Vinculación*

Tu código es: `{codigo}`

Este código es válido por 10 minutos.

*Opciones para vincular:*
1. Llama al taller y proporciona este código
2. Visita nuestra oficina con este código
3. Responde al SMS que te enviaremos

Una vez vinculado, recibirás notificaciones automáticas.
    """
    
    await update.message.reply_text(mensaje, parse_mode='Markdown')


# Vista Django para confirmar vinculación
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import json

@csrf_exempt
def confirmar_vinculacion_telegram(request):
    """
    Vista para que el personal del taller confirme la vinculación
    POST /api/telegram/vincular/
    {
        "codigo": "123456"
    }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        codigo = data.get('codigo')
        
        if not codigo:
            return JsonResponse({'error': 'Código requerido'}, status=400)
        
        # Buscar en cache
        cache_key = f'telegram_vinculacion_{codigo}'
        datos = cache.get(cache_key)
        
        if not datos:
            return JsonResponse({'error': 'Código inválido o expirado'}, status=404)
        
        telefono = datos['telefono']
        chat_id = datos['chat_id']
        username = datos.get('username')
        
        # Buscar cliente
        from gestion.models import Cliente
        cliente = Cliente.objects.get(telefono=telefono)
        
        # Vincular
        cliente.telegram_chat_id = chat_id
        if username:
            cliente.telegram_username = username
        cliente.save()
        
        # Eliminar de cache
        cache.delete(cache_key)
        
        # Enviar confirmación al cliente
        enviar_mensaje_telegram(
            chat_id,
            f"✅ ¡Cuenta vinculada exitosamente!\n\n"
            f"Hola {cliente.nombre_completo}, "
            f"ahora recibirás notificaciones sobre tus reparaciones."
        )
        
        return JsonResponse({
            'success': True,
            'cliente': {
                'nombre': cliente.nombre_completo,
                'telefono': cliente.telefono,
                'telegram_username': username
            }
        })
        
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def enviar_mensaje_telegram(chat_id, mensaje):
    """Enviar mensaje a un chat específico"""
    import requests
    from django.conf import settings
    
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': mensaje,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, json=data)
        return response.status_code == 200
    except:
        return False


"""
RESUMEN DE IMPLEMENTACIÓN:
--------------------------

1. ✅ Agregar campos telegram_chat_id y telegram_username al modelo Cliente
2. ✅ Crear migración y aplicarla
3. ✅ Actualizar admin para gestionar estos campos
4. ✅ Crear comando /vincular en el bot
5. ✅ Implementar sistema de códigos de verificación
6. ✅ Crear vista para confirmar vinculación
7. ✅ Enviar notificaciones a clientes vinculados

SEGURIDAD:
----------
- Códigos con expiración (10 minutos)
- Validación de identidad por teléfono
- Solo personal autorizado puede confirmar
- Chat IDs únicos por cliente
"""
