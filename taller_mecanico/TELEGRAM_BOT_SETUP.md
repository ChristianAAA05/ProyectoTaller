# Configuración del Bot de Telegram - Guía para el Equipo

## 🤖 Resumen

Este proyecto incluye un bot de Telegram para que los clientes puedan agendar citas automáticamente. Cada desarrollador necesita su propio bot de prueba para evitar conflictos.

---

## 📋 Pasos para Configurar tu Bot Local

### 1. Crear tu Bot en Telegram

1. Abre Telegram y busca `@BotFather`
2. Envía `/newbot`
3. Sigue las instrucciones:
   - **Nombre del bot**: `Taller Mecánico [TuNombre]` (ej: "Taller Mecánico Juan")
   - **Username**: `taller_mecanico_[tunombre]_bot` (ej: `taller_mecanico_juan_bot`)
4. **Copia el token** que te proporciona (se ve como: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Configurar Variables de Entorno

1. Copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```

2. Edita el archivo `.env` y reemplaza el token:
   ```
   # Token del bot de Telegram (obtener de @BotFather)
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

### 3. Instalar Dependencias

```bash
# Activar entorno virtual
source ../.venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Ejecutar el Bot

```bash
python manage.py run_telegram_bot
```

### 5. Probar el Bot

1. Busca tu bot en Telegram
2. Envía `/start`
3. Sigue el flujo completo de agendar cita

---

## 🔐 Seguridad Importante

### ✅ Lo que está protegido:
- **`.env`** está en `.gitignore` (no se sube al repositorio)
- **Tokens** se cargan desde variables de entorno
- **Cada desarrollador** tiene su propio bot de prueba

### ❌ Lo que NUNCA debes hacer:
- **NO** compartir tu token del bot
- **NO** subir el archivo `.env` al repositorio
- **NO** usar el mismo bot que otro desarrollador al mismo tiempo

---

## 👥 Trabajo en Equipo

### ¿Por qué cada desarrollador necesita su propio bot?

**Solo una instancia del bot puede correr por token.** Si dos desarrolladores usan el mismo token:
- El bot se desconectará constantemente
- Los mensajes se perderán
- No podrás probar correctamente

### Flujo recomendado:

1. **Desarrollo individual**: Cada uno con su bot de prueba
2. **Integración**: Probar con datos de prueba en base de datos local
3. **Producción**: Bot oficial con token seguro en servidor

---

## 🚀 Despliegue en Producción

### Para producción (NO usar en desarrollo):

1. **Variables de entorno del servidor** (no archivo .env):
   ```bash
   export TELEGRAM_BOT_TOKEN="token_de_produccion"
   ```

2. **Bot oficial separado** de los bots de desarrollo
3. **Configurar webhooks** en lugar de polling
4. **Usar supervisor/systemd** para mantener el bot corriendo

---

## 🐛 Problemas Comunes

### "Bot no responde"
- Verifica que el token esté correcto en `.env`
- Asegúrate de que solo una instancia esté corriendo
- Revisa la consola para errores

### "Error de token"
- El token debe tener el formato: `numbers:letters`
- Verifica que no haya espacios extra

### "Conexión rechazada"
- Puede que otra instancia esté usando el mismo token
- Detén todas las instancias y reinicia

---

## 📞 Contacto y Soporte

Si tienes problemas:
1. Revisa este documento
2. Consulta los logs en la consola
3. Contacta al líder del proyecto

---

## 🔄 Actualizaciones

Cuando actualices el proyecto:
1. Sincroniza los cambios del repositorio
2. Reinstala dependencias si es necesario
3. No necesitas recrear tu bot (solo si hay cambios estructurales)

---

**🎯 Listo! Con estos pasos tendrás tu bot funcionando para desarrollo.**
