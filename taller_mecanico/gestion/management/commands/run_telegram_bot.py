"""
Management command para ejecutar el bot de Telegram del taller mecánico.

Este comando inicia el bot que permite a los clientes:
- Recibir un saludo de bienvenida
- Ser guiados paso a paso para solicitar reparaciones
- Seleccionar servicios con botones
- Ingresar información de vehículo y contacto
- Seleccionar fecha y hora programada
- Confirmar y guardar la solicitud como reparación disponible para mecánicos

Uso:
    python manage.py run_telegram_bot

El bot se ejecutará en modo polling (ideal para desarrollo).
Para producción, considerar cambiar a webhooks.
"""

import os
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from asgiref.sync import sync_to_async
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes
from gestion.models import Cliente, Vehiculo, Servicio, Reparacion

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Estados de la conversación
START, PHONE, NAME, VEHICLE_BRAND, VEHICLE_MODEL, VEHICLE_YEAR, VEHICLE_PLATE, SERVICE_SELECT, DATE_SELECT, TIME_SELECT, CONFIRMATION = range(11)


class Command(BaseCommand):
    help = 'Ejecuta el bot de Telegram para el taller mecánico'

    def handle(self, *args, **options):
        """Inicia el bot de Telegram"""
        
        # Obtener token del bot (debería estar en settings.py o variables de entorno)
        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        if not bot_token:
            self.stdout.write(
                self.style.ERROR('❌ ERROR: No se encontró TELEGRAM_BOT_TOKEN en settings.py')
            )
            return
        
        # Crear aplicación del bot
        application = Application.builder().token(bot_token).build()
        
        # Crear manejador de conversación
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start_command)],
            states={
                START: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
                PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
                NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_vehicle_brand)],
                VEHICLE_BRAND: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_vehicle_model)],
                VEHICLE_MODEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_vehicle_year)],
                VEHICLE_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_vehicle_plate)],
                VEHICLE_PLATE: [CallbackQueryHandler(select_service)],
                SERVICE_SELECT: [CallbackQueryHandler(select_service)],
                DATE_SELECT: [CallbackQueryHandler(select_date)],
                TIME_SELECT: [CallbackQueryHandler(select_time)],
                CONFIRMATION: [CallbackQueryHandler(confirm_appointment)],
            },
            fallbacks=[CommandHandler('cancel', cancel_command)],
            per_user=False,
            per_chat=True,
            allow_reentry=True
        )

        # Agregar manejadores
        application.add_handler(conv_handler)
        application.add_handler(CommandHandler('help', help_command))
        
        # Mensaje de inicio
        self.stdout.write(self.style.SUCCESS('🤖 Bot de Telegram iniciado...'))
        
        # Iniciar el bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Muestra mensaje de ayuda"""
    help_text = """
🛠️ *Ayuda del Bot del Taller Mecánico*

📋 *Comandos disponibles:*
/start - Iniciar solicitud de reparación
/cancel - Cancelar proceso actual
/help - Mostrar esta ayuda

🔄 *Flujo de solicitud:*
1. Ingresa tu teléfono 📞
2. Ingresa tu nombre 👤
3. Datos del vehículo 🚗
4. Selecciona servicio 🔧
5. Selecciona fecha y hora 📅🕐
6. Confirma solicitud ✅

📱 *Una vez confirmada, tu solicitud aparecerá*
*inmediatamente en Reparaciones Disponibles*
*para que los mecánicos puedan tomarla.*

❓ *¿Necesitas ayuda?* Contacta al taller directamente.
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia la conversación para solicitar reparación"""
    user = update.effective_user
    
    # Mensaje de bienvenida
    welcome_message = f"""
🔧 *¡Bienvenido al Taller Mecánico!* 🔧

Hola {user.first_name}! 👋

Soy el asistente virtual y te ayudaré a solicitar tu reparación.

📋 *Proceso simple:*
• Teléfono de contacto
• Nombre completo
• Información del vehículo
• Servicio requerido
• Fecha y hora programada

🤖 *Tu solicitud aparecerá inmediatamente* 
*en Reparaciones Disponibles para nuestros mecánicos.*

📞 *Por favor, ingresa tu número de teléfono:*
    """
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown')
    return START


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Obtiene el número de teléfono del cliente"""
    phone = update.message.text.strip()
    
    # Validación básica de teléfono
    if len(phone) < 8 or not phone.replace(' ', '').replace('-', '').replace('+', '').isdigit():
        await update.message.reply_text(
            "❌ Por favor, ingresa un número de teléfono válido:\n"
            "Ejemplo: 123456789 o +56912345678"
        )
        return START
    
    context.user_data['phone'] = phone
    
    await update.message.reply_text(
        f"✅ Teléfono guardado: {phone}\n\n"
        "📝 Ahora, por favor ingresa tu nombre completo:"
    )
    
    return PHONE


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Obtiene el nombre del cliente"""
    name = update.message.text.strip()
    
    if len(name) < 3:
        await update.message.reply_text(
            "❌ Por favor, ingresa tu nombre completo (mínimo 3 caracteres):"
        )
        return PHONE
    
    context.user_data['name'] = name
    
    await update.message.reply_text(
        f"✅ Nombre guardado: {name}\n\n"
        "🚗 Ahora necesito información de tu vehículo.\n\n"
        "📋 *Marca del vehículo:* (Ej: Toyota, Ford, BMW)"
    )
    
    return NAME


async def get_vehicle_brand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Obtiene la marca del vehículo"""
    brand = update.message.text.strip()
    
    if len(brand) < 2:
        await update.message.reply_text(
            "❌ Por favor, ingresa una marca válida (mínimo 2 caracteres):"
        )
        return NAME
    
    context.user_data['vehicle_brand'] = brand
    
    await update.message.reply_text(
        f"✅ Marca guardada: {brand}\n\n"
        "📋 *Modelo del vehículo:* (Ej: Corolla, Mustang, X5)"
    )
    
    return VEHICLE_BRAND


async def get_vehicle_model(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Obtiene el modelo del vehículo"""
    model = update.message.text.strip()
    
    if len(model) < 2:
        await update.message.reply_text(
            "❌ Por favor, ingresa un modelo válido (mínimo 2 caracteres):"
        )
        return VEHICLE_BRAND
    
    context.user_data['vehicle_model'] = model
    
    await update.message.reply_text(
        f"✅ Modelo guardado: {model}\n\n"
        "📋 *Año del vehículo:* (Ej: 2020, 2019, 2021)"
    )
    
    return VEHICLE_MODEL


async def get_vehicle_year(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Obtiene el año del vehículo"""
    year_text = update.message.text.strip()
    
    # Validar que sea un año válido
    try:
        year = int(year_text)
        current_year = 2024
        if year < 1900 or year > current_year + 1:
            await update.message.reply_text(
                f"❌ Por favor, ingresa un año válido entre 1900 y {current_year + 1}:"
            )
            return VEHICLE_MODEL
    except ValueError:
        await update.message.reply_text(
            "❌ Por favor, ingresa un año válido (solo números):"
        )
        return VEHICLE_MODEL
    
    context.user_data['vehicle_year'] = year
    
    await update.message.reply_text(
        f"✅ Año guardado: {year}\n\n"
        "📋 *Placa del vehículo:* (Ej: ABC123, XYZ999)"
    )
    
    return VEHICLE_YEAR


async def get_vehicle_plate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Obtiene la placa del vehículo y muestra servicios disponibles"""
    plate = update.message.text.strip()
    
    # Validación flexible de placa
    if len(plate) < 1 or len(plate) > 20:
        await update.message.reply_text(
            "❌ Por favor, ingresa una placa válida (máximo 20 caracteres):"
        )
        return VEHICLE_YEAR
    
    context.user_data['vehicle_plate'] = plate
    
    # Obtener servicios disponibles
    try:
        servicios = await sync_to_async(list)(Servicio.objects.all())
        
        if not servicios:
            await update.message.reply_text(
                "❌ No hay servicios disponibles en este momento.\n"
                "Por favor, contacta al taller directamente."
            )
            return ConversationHandler.END
        
        # Crear botones para servicios
        keyboard = []
        for servicio in servicios:
            keyboard.append([InlineKeyboardButton(
                f"{servicio.nombre_servicio} - ${servicio.costo}",
                callback_data=f"service_{servicio.id}"
            )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        service_message = f"✅ Placa: {plate}\n\n🔧 *Selecciona el servicio que necesitas:*\n"
        
        await update.message.reply_text(
            service_message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
        return SERVICE_SELECT
        
    except Exception as e:
        logger.error(f"❌ Error al obtener servicios: {e}")
        await update.message.reply_text(
            "❌ Error al cargar los servicios. Por favor, intenta más tarde."
        )
        return ConversationHandler.END


async def select_service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Maneja la selección del servicio y va a selección de fecha"""
    query = update.callback_query
    await query.answer()
    
    service_id = query.data.split('_')[1]
    
    try:
        servicio = await sync_to_async(Servicio.objects.get)(id=service_id)
        context.user_data['service'] = servicio
        
        # Preparar mensaje y mostrar calendario
        service_message = (
            f"✅ *Servicio seleccionado:*\n"
            f"🔧 {servicio.nombre_servicio}\n"
            f"💰 Costo: ${servicio.costo}\n"
            f"⏱️ Duración estimada: {servicio.duracion} minutos\n\n"
            f"📅 *Ahora selecciona la fecha para llevar tu vehículo:*\n"
        )
        
        await query.edit_message_text(
            service_message,
            parse_mode='Markdown',
            reply_markup=create_date_keyboard()
        )
        
        return DATE_SELECT
        
    except Exception as e:
        logger.error(f"❌ Error al obtener servicio: {e}")
        await query.edit_message_text(
            "❌ Servicio no encontrado. Por favor, selecciona otro."
        )
        return VEHICLE_PLATE


def create_date_keyboard():
    """Crea un teclado con las próximas fechas disponibles"""
    from datetime import datetime, timedelta
    
    keyboard = []
    current_date = datetime.now()
    
    # Mostrar próximos 7 días
    for i in range(1, 8):
        date = current_date + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        display_str = date.strftime("%d/%m/%Y (%A)")
        keyboard.append([InlineKeyboardButton(
            display_str,
            callback_data=f"date_{date_str}"
        )])
    
    return InlineKeyboardMarkup(keyboard)


async def select_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Maneja la selección de fecha y muestra horas disponibles"""
    query = update.callback_query
    await query.answer()
    
    # Extraer fecha del callback_data
    if query.data.startswith('date_'):
        date_str = query.data[5:]  # Remover 'date_' del inicio
    else:
        date_str = query.data.split('_')[1] if len(query.data.split('_')) > 1 else query.data
    
    context.user_data['date'] = date_str
    
    # Convertir string a fecha para mostrar
    from datetime import datetime
    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        display_date = selected_date.strftime("%d/%m/%Y")
    except ValueError as e:
        logger.error(f"❌ Error al parsear fecha '{date_str}': {e}")
        await query.edit_message_text(
            f"❌ Error al procesar la fecha: {date_str}\n"
            f"Por favor, selecciona otra fecha."
        )
        return SERVICE_SELECT
    
    # Obtener horas disponibles
    available_hours = await get_available_hours(date_str)
    
    if not available_hours:
        await query.edit_message_text(
            f"❌ No hay horas disponibles para el {display_date}.\n"
            "Por favor, selecciona otra fecha."
        )
        return SERVICE_SELECT
    
    # Crear teclado con horas disponibles
    keyboard = []
    for hour in available_hours:
        keyboard.append([InlineKeyboardButton(
            hour,
            callback_data=f"time_{hour}"
        )])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"📅 Fecha seleccionada: {display_date}\n\n"
        f"🕐 *Selecciona la hora para tu cita:*\n",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
    
    return TIME_SELECT


async def get_available_hours(date_str):
    """Obtiene horas disponibles para una fecha específica"""
    # Horas de trabajo (8:00 AM - 6:00 PM)
    work_hours = []
    for hour in range(8, 19):  # 8 AM a 6 PM
        work_hours.append(f"{hour:02d}:00")
    
    # Obtener horas ya ocupadas en esa fecha
    try:
        # Función síncrona para obtener horas ocupadas
        def get_occupied_hours_sync():
            return list(Reparacion.objects.filter(
                fecha_programada=date_str,
                estado_reparacion__in=['pendiente', 'en_progreso']
            ).values_list('hora_programada', flat=True))
        
        occupied_hours = await sync_to_async(get_occupied_hours_sync)()
        
        # Convertir a string para comparación
        occupied_str = [str(h) for h in occupied_hours if h is not None]
        
        # Filtrar horas disponibles
        available = [h for h in work_hours if h not in occupied_str]
        
        return available
        
    except Exception as e:
        logger.error(f"Error al obtener horas ocupadas: {e}")
        return work_hours  # Devolver todas si hay error


async def select_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Maneja la selección de hora y va a confirmación"""
    query = update.callback_query
    await query.answer()
    
    time_str = query.data.split('_')[1]
    context.user_data['time'] = time_str
    
    # Preparar resumen completo
    service = context.user_data['service']
    summary = (
        f"📋 *RESUMEN DE TU SOLICITUD* 📋\n\n"
        f"👤 *Cliente:* {context.user_data['name']}\n"
        f"📱 *Teléfono:* {context.user_data['phone']}\n\n"
        f"🚗 *Vehículo:* {context.user_data['vehicle_brand']} {context.user_data['vehicle_model']} ({context.user_data['vehicle_year']})\n"
        f"🔢 *Placa:* {context.user_data['vehicle_plate']}\n\n"
        f"🔧 *Servicio:* {service.nombre_servicio}\n"
        f"💰 *Costo:* ${service.costo}\n"
        f"⏱️ *Duración:* {service.duracion} minutos\n\n"
        f"📅 *Fecha programada:* {context.user_data['date']}\n"
        f"🕐 *Hora:* {time_str}\n\n"
        f"🤖 *Esta reparación aparecerá en Reparaciones Disponibles*\n"
        f"con la fecha y hora programadas.\n\n"
        f"¿Confirmas esta solicitud?"
    )
    
    # Crear botones de confirmación
    keyboard = [
        [InlineKeyboardButton("✅ Sí, confirmar", callback_data="confirm_yes")],
        [InlineKeyboardButton("❌ No, cancelar", callback_data="confirm_no")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        summary,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
    
    return CONFIRMATION


async def confirm_appointment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Confirma y crea la reparación en la base de datos"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'confirm_yes':
        # Preparar datos para crear la reparación
        repair_data = {
            'name': context.user_data['name'],
            'phone': context.user_data['phone'],
            'vehicle_brand': context.user_data['vehicle_brand'],
            'vehicle_model': context.user_data['vehicle_model'],
            'vehicle_year': context.user_data['vehicle_year'],
            'vehicle_plate': context.user_data['vehicle_plate'],
            'service': context.user_data['service'],
            'date': context.user_data['date'],
            'time': context.user_data['time']
        }
        
        # Crear la reparación (await correctamente)
        success = await create_repair_in_db(repair_data)
        
        if success:
            await query.edit_message_text(
                "✅ *¡SOLICITUD CREADA CON ÉXITO!*\n\n"
                "🤖 Tu solicitud de reparación ha sido enviada\n"
                "y aparecerá inmediatamente en\n"
                "Reparaciones Disponibles para los mecánicos.\n\n"
                f"📅 *Fecha programada:* {context.user_data['date']}\n"
                f"🕐 *Hora:* {context.user_data['time']}\n\n"
                "📞 Nos contactaremos contigo pronto.\n\n"
                "¡Gracias por usar nuestro servicio!",
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(
                "❌ *ERROR AL CREAR SOLICITUD*\n\n"
                "Hubo un problema al procesar tu solicitud.\n"
                "Por favor, intenta nuevamente más tarde\n"
                "o contacta directamente al taller."
            )
    else:  # confirm_no
        await query.edit_message_text(
            "❌ *SOLICITUD CANCELADA*\n\n"
            "No te preocupes, puedes solicitar tu reparación\n"
            "cuando quieras usando /start"
        )
    
    return ConversationHandler.END


async def create_repair_in_db(data):
    """Crea la reparación en la base de datos para que aparezca en Reparaciones Disponibles"""
    try:
        # Obtener o crear cliente usando teléfono como identificador único
        try:
            cliente = await sync_to_async(Cliente.objects.get)(telefono=data['phone'])
            # Actualizar nombre si es diferente
            if cliente.nombre != data['name'].split()[0]:
                cliente.nombre = data['name'].split()[0]
                cliente.apellido = ' '.join(data['name'].split()[1:]) if len(data['name'].split()) > 1 else ''
                await sync_to_async(cliente.save)()
        except Cliente.DoesNotExist:
            # Crear nuevo cliente con email temporal único
            import uuid
            temp_email = f"telegram_{data['phone']}_{uuid.uuid4().hex[:8]}@bot.local"
            cliente = await sync_to_async(Cliente.objects.create)(
                correo_electronico=temp_email,
                nombre=data['name'].split()[0],
                apellido=' '.join(data['name'].split()[1:]) if len(data['name'].split()) > 1 else '',
                telefono=data['phone'],
                direccion='Cliente Telegram'
            )
        
        # Verificar si el vehículo ya existe para este cliente
        try:
            vehiculo = await sync_to_async(Vehiculo.objects.get)(
                cliente=cliente,
                placa=data['vehicle_plate']
            )
            # Actualizar datos del vehículo si son diferentes
            if (vehiculo.marca != data['vehicle_brand'] or 
                vehiculo.modelo != data['vehicle_model'] or 
                vehiculo.año != data['vehicle_year']):
                vehiculo.marca = data['vehicle_brand']
                vehiculo.modelo = data['vehicle_model']
                vehiculo.año = data['vehicle_year']
                await sync_to_async(vehiculo.save)()
        except Vehiculo.DoesNotExist:
            # Crear nuevo vehículo
            vehiculo = await sync_to_async(Vehiculo.objects.create)(
                cliente=cliente,
                marca=data['vehicle_brand'],
                modelo=data['vehicle_model'],
                año=data['vehicle_year'],
                placa=data['vehicle_plate']
            )
        
        # Convertir hora string a time object
        from datetime import datetime
        time_obj = datetime.strptime(data['time'], "%H:%M").time()
        
        # Crear reparación directamente para que aparezca en Reparaciones Disponibles
        reparacion = await sync_to_async(Reparacion.objects.create)(
            vehiculo=vehiculo,
            servicio=data['service'],
            mecanico_asignado=None,  # Sin asignar para que aparezca como disponible
            condicion_vehiculo='regular',  # Condición por defecto
            estado_reparacion='pendiente',  # Estado pendiente para que los mecánicos puedan tomarla
            fecha_programada=data['date'],  # Fecha programada por el cliente
            hora_programada=time_obj  # Hora programada por el cliente
        )
        
        logger.info(f"✅ Reparación creada exitosamente: Cliente {cliente.nombre} ({cliente.telefono}), Vehículo {vehiculo.marca} {vehiculo.modelo} ({vehiculo.placa}), Reparación ID {reparacion.id}, Programada para {data['date']} a las {data['time']}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error al crear reparación en BD: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela la conversación actual"""
    await update.message.reply_text(
        "❌ *Proceso cancelado*\n\n"
        "Si quieres solicitar una reparación, usa /start nuevamente."
    )
    return ConversationHandler.END
