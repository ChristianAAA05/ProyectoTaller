"""
Ejemplo de implementación de Bot de Telegram para Taller Mecánico
Archivo: taller_mecanico/gestion/telegram_bot.py
"""

import os
from telegram import Update
from telegram.ext import ContextTypes
from django.conf import settings

# Importar modelos de Django
from gestion.models import Reparacion, Cliente, Vehiculo


# ==================== COMANDOS DEL BOT ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /start - Mensaje de bienvenida
    """
    mensaje = """
🔧 *Bienvenido al Taller Mecánico Bot* 🔧

¿En qué puedo ayudarte?

*Comandos disponibles:*
/estado - Consultar estado de tu reparación
/agendar - Agendar una cita
/contacto - Información de contacto
/help - Ver esta ayuda

Escribe el número de placa de tu vehículo para consultar el estado.
    """
    await update.message.reply_text(mensaje, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /help - Ayuda
    """
    mensaje = """
📋 *Ayuda - Taller Mecánico*

*Comandos disponibles:*

/estado - Consultar estado de reparación
   Ejemplo: /estado ABC123

/agendar - Solicitar una cita
   Te guiaremos paso a paso

/contacto - Ver información del taller
   Teléfono, dirección, horarios

/start - Volver al menú principal

*Consulta rápida:*
También puedes escribir directamente la placa de tu vehículo (ej: ABC123) y te mostraré el estado de la reparación.

¿Necesitas ayuda? Contáctanos: +595 XXX XXXXXX
    """
    await update.message.reply_text(mensaje, parse_mode='Markdown')


async def estado_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /estado PLACA - Consultar estado de reparación
    """
    if not context.args:
        await update.message.reply_text(
            "Por favor proporciona el número de placa.\n"
            "Ejemplo: /estado ABC123"
        )
        return
    
    placa = context.args[0].upper()
    
    try:
        # Buscar vehículo por placa
        vehiculo = Vehiculo.objects.get(placa=placa)
        
        # Obtener última reparación
        reparacion = Reparacion.objects.filter(vehiculo=vehiculo).order_by('-fecha_ingreso').first()
        
        if not reparacion:
            await update.message.reply_text(
                f"No se encontraron reparaciones para el vehículo {placa}."
            )
            return
        
        # Crear mensaje con el estado
        estado_emoji = {
            'pendiente': '🟡',
            'en_progreso': '🔵',
            'en_espera': '🟠',
            'revision': '🟣',
            'completada': '🟢',
            'cancelada': '🔴'
        }
        
        emoji = estado_emoji.get(reparacion.estado_reparacion, '⚪')
        
        mensaje = f"""
🚗 *Estado de tu Reparación*

*Vehículo:* {vehiculo.marca} {vehiculo.modelo}
*Placa:* {vehiculo.placa}
*Cliente:* {vehiculo.cliente.nombre_completo}

*Servicio:* {reparacion.servicio.nombre_servicio}
*Estado:* {emoji} {reparacion.get_estado_reparacion_display()}
*Fecha de Ingreso:* {reparacion.fecha_ingreso.strftime('%d/%m/%Y %H:%M')}

{f"*Mecánico Asignado:* {reparacion.mecanico_asignado.nombre}" if reparacion.mecanico_asignado else ""}
{f"*Fecha de Salida:* {reparacion.fecha_salida.strftime('%d/%m/%Y %H:%M')}" if reparacion.fecha_salida else ""}

{f"*Notas:* {reparacion.notas[:200]}..." if reparacion.notas else ""}

Para más información, contáctanos: +595 XXX XXXXXX
        """
        
        await update.message.reply_text(mensaje, parse_mode='Markdown')
        
    except Vehiculo.DoesNotExist:
        await update.message.reply_text(
            f"❌ No se encontró ningún vehículo con la placa *{placa}*.\n"
            "Por favor verifica el número de placa.",
            parse_mode='Markdown'
        )
    except Exception as e:
        await update.message.reply_text(
            "❌ Ocurrió un error al consultar el estado. "
            "Por favor intenta nuevamente más tarde."
        )


async def contacto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /contacto - Información del taller
    """
    mensaje = """
📞 *Información de Contacto*

*Taller Mecánico*
🏢 Dirección: [Tu dirección aquí]
📱 Teléfono: +595 XXX XXXXXX
📧 Email: info@tallermecanico.com

*Horarios de Atención:*
🕐 Lunes a Viernes: 8:00 AM - 6:00 PM
🕐 Sábados: 8:00 AM - 12:00 PM
🕐 Domingos: Cerrado

*Redes Sociales:*
📘 Facebook: /tallermecanico
📷 Instagram: @tallermecanico

¡Estamos para servirte! 🔧
    """
    await update.message.reply_text(mensaje, parse_mode='Markdown')


async def agendar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /agendar - Solicitar cita
    """
    mensaje = """
📅 *Agendar una Cita*

Para agendar una cita, necesitamos la siguiente información:

1. Tu nombre completo
2. Número de placa del vehículo
3. Servicio requerido
4. Fecha preferida
5. Teléfono de contacto

Por favor contáctanos directamente:
📱 +595 XXX XXXXXX
📧 citas@tallermecanico.com

O visita nuestra web para agendar en línea.

¡Te esperamos! 🔧
    """
    await update.message.reply_text(mensaje, parse_mode='Markdown')


async def mensaje_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Procesar mensajes de texto (ej: placas de vehículos)
    """
    texto = update.message.text.strip().upper()
    
    # Si parece una placa (4-10 caracteres alfanuméricos)
    if 4 <= len(texto) <= 10 and texto.replace('-', '').replace(' ', '').isalnum():
        # Simular comando /estado
        context.args = [texto]
        await estado_command(update, context)
    else:
        await update.message.reply_text(
            "No entendí tu mensaje. Usa /help para ver los comandos disponibles."
        )


# ==================== FUNCIONES AUXILIARES ====================

def enviar_notificacion_reparacion_completada(reparacion_id):
    """
    Enviar notificación cuando una reparación se completa
    """
    import requests
    
    try:
        reparacion = Reparacion.objects.get(id=reparacion_id)
        cliente = reparacion.vehiculo.cliente
        
        # Aquí deberías tener el chat_id del cliente guardado en la base de datos
        # Por ahora es un placeholder
        chat_id = cliente.telegram_chat_id if hasattr(cliente, 'telegram_chat_id') else None
        
        if not chat_id:
            return False
        
        mensaje = f"""
✅ *¡Tu vehículo está listo!*

Hola {cliente.nombre_completo},

Tu *{reparacion.vehiculo.marca} {reparacion.vehiculo.modelo}* (Placa: {reparacion.vehiculo.placa}) ha sido reparado y está listo para ser retirado.

*Servicio realizado:* {reparacion.servicio.nombre_servicio}
*Fecha de finalización:* {reparacion.fecha_salida.strftime('%d/%m/%Y %H:%M')}

Por favor pasa a retirar tu vehículo en nuestro horario de atención.

¡Gracias por confiar en nosotros! 🔧
        """
        
        # Enviar mensaje via API de Telegram
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': mensaje,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, json=data)
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error enviando notificación: {e}")
        return False


def enviar_notificacion_mecanico_asignado(reparacion_id):
    """
    Notificar al mecánico cuando se le asigna una reparación
    """
    import requests
    
    try:
        reparacion = Reparacion.objects.get(id=reparacion_id)
        mecanico = reparacion.mecanico_asignado
        
        # Chat ID del mecánico (debe estar guardado en la BD)
        chat_id = mecanico.telegram_chat_id if hasattr(mecanico, 'telegram_chat_id') else None
        
        if not chat_id:
            return False
        
        mensaje = f"""
🔔 *Nueva Reparación Asignada*

Hola {mecanico.nombre},

Se te ha asignado una nueva reparación:

*Vehículo:* {reparacion.vehiculo.marca} {reparacion.vehiculo.modelo}
*Placa:* {reparacion.vehiculo.placa}
*Cliente:* {reparacion.vehiculo.cliente.nombre_completo}
*Servicio:* {reparacion.servicio.nombre_servicio}
*Estado:* {reparacion.get_estado_reparacion_display()}

Ingresa al sistema para ver más detalles.
        """
        
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': mensaje,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, json=data)
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error enviando notificación: {e}")
        return False


# ==================== PROCESAMIENTO DE WEBHOOK ====================

def procesar_mensaje_telegram(data):
    """
    Procesar mensajes entrantes del webhook
    Esta función se llama desde la vista telegram_webhook
    """
    # Esta es una implementación básica
    # Para producción, usa la biblioteca python-telegram-bot completa
    pass


# ==================== INTEGRACIÓN CON SEÑALES DE DJANGO ====================

"""
Para enviar notificaciones automáticamente cuando cambia el estado de una reparación,
agregar en gestion/signals.py:

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reparacion
from .telegram_bot import (
    enviar_notificacion_reparacion_completada,
    enviar_notificacion_mecanico_asignado
)

@receiver(post_save, sender=Reparacion)
def notificar_cambio_reparacion(sender, instance, created, **kwargs):
    # Si se completó la reparación
    if instance.estado_reparacion == 'completada' and instance.fecha_salida:
        enviar_notificacion_reparacion_completada(instance.id)
    
    # Si se asignó un mecánico
    if instance.mecanico_asignado and not created:
        enviar_notificacion_mecanico_asignado(instance.id)
"""
