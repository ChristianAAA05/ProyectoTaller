#!/usr/bin/env python
"""
Script para ejecutar el Bot de Telegram en modo Polling (desarrollo local)
Ubicación sugerida: taller_mecanico/run_telegram_bot.py

USO:
    python run_telegram_bot.py
"""

import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'taller_mecanico'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taller_mecanico.settings')
django.setup()

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from django.conf import settings


# ==================== COMANDOS DEL BOT ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    mensaje = """
🔧 *Bienvenido al Taller Mecánico Bot* 🔧

¿En qué puedo ayudarte?

*Comandos disponibles:*
/estado <placa> - Consultar estado de reparación
/agendar - Agendar una cita
/contacto - Información de contacto
/help - Ver esta ayuda

Escribe la placa de tu vehículo para consultar el estado.
    """
    await update.message.reply_text(mensaje, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    mensaje = """
📋 *Ayuda - Taller Mecánico*

*Comandos:*
/estado <placa> - Ver estado de reparación
/agendar - Solicitar cita
/contacto - Info del taller
/start - Menú principal

Escribe la placa directamente para consulta rápida.
    """
    await update.message.reply_text(mensaje, parse_mode='Markdown')


async def estado_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /estado para consultar reparaciones"""
    from gestion.models import Vehiculo, Reparacion
    
    if not context.args:
        await update.message.reply_text(
            "Por favor proporciona la placa.\nEjemplo: /estado ABC123"
        )
        return
    
    placa = context.args[0].upper()
    
    try:
        vehiculo = Vehiculo.objects.get(placa=placa)
        reparacion = Reparacion.objects.filter(
            vehiculo=vehiculo
        ).order_by('-fecha_ingreso').first()
        
        if not reparacion:
            await update.message.reply_text(
                f"No hay reparaciones para {placa}"
            )
            return
        
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
🚗 *Estado de Reparación*

*Vehículo:* {vehiculo.marca} {vehiculo.modelo}
*Placa:* {vehiculo.placa}
*Cliente:* {vehiculo.cliente.nombre_completo}

*Servicio:* {reparacion.servicio.nombre_servicio}
*Estado:* {emoji} {reparacion.get_estado_reparacion_display()}
*Ingreso:* {reparacion.fecha_ingreso.strftime('%d/%m/%Y')}

{f"*Mecánico:* {reparacion.mecanico_asignado.nombre}" if reparacion.mecanico_asignado else ""}
{f"*Finalizado:* {reparacion.fecha_salida.strftime('%d/%m/%Y')}" if reparacion.fecha_salida else ""}

📞 Consultas: +595 XXX XXXXXX
        """
        
        await update.message.reply_text(mensaje, parse_mode='Markdown')
        
    except Vehiculo.DoesNotExist:
        await update.message.reply_text(
            f"❌ No se encontró vehículo con placa *{placa}*",
            parse_mode='Markdown'
        )
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text(
            "❌ Error al consultar. Intenta nuevamente."
        )


async def contacto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /contacto"""
    mensaje = """
📞 *Taller Mecánico*

🏢 Dirección: [Tu dirección]
📱 Teléfono: +595 XXX XXXXXX
📧 Email: info@taller.com

*Horarios:*
🕐 Lun-Vie: 8:00-18:00
🕐 Sábados: 8:00-12:00
🕐 Domingos: Cerrado

🔧 ¡Estamos para servirte!
    """
    await update.message.reply_text(mensaje, parse_mode='Markdown')


async def agendar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /agendar"""
    mensaje = """
📅 *Agendar Cita*

Para agendar, contáctanos:
📱 +595 XXX XXXXXX
📧 citas@taller.com

O visita nuestra web.

¡Te esperamos! 🔧
    """
    await update.message.reply_text(mensaje, parse_mode='Markdown')


async def mensaje_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Procesar texto (placas)"""
    from gestion.models import Vehiculo
    
    texto = update.message.text.strip().upper()
    
    # Si parece una placa
    if 4 <= len(texto) <= 10 and texto.replace('-', '').isalnum():
        context.args = [texto]
        await estado_command(update, context)
    else:
        await update.message.reply_text(
            "No entendí. Usa /help para ver comandos."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejar errores"""
    print(f"Error: {context.error}")


# ==================== MAIN ====================

def main():
    """Función principal"""
    
    # Obtener token
    TOKEN = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    
    if not TOKEN:
        print("❌ ERROR: TELEGRAM_BOT_TOKEN no configurado en settings.py")
        print("Agrega TELEGRAM_BOT_TOKEN a tu archivo .env")
        return
    
    print("🤖 Iniciando Taller Mecánico Bot...")
    print(f"Token: {TOKEN[:10]}...{TOKEN[-5:]}")
    
    # Crear aplicación
    app = Application.builder().token(TOKEN).build()
    
    # Registrar comandos
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("estado", estado_command))
    app.add_handler(CommandHandler("contacto", contacto_command))
    app.add_handler(CommandHandler("agendar", agendar_command))
    
    # Manejar mensajes de texto
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        mensaje_texto
    ))
    
    # Manejar errores
    app.add_error_handler(error_handler)
    
    # Iniciar bot
    print("✅ Bot en modo polling (desarrollo local)")
    print("📱 Busca tu bot en Telegram y envía /start")
    print("Presiona Ctrl+C para detener\n")
    
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Bot detenido")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
