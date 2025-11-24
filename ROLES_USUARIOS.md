# Gestión de Roles de Usuario

## Usuarios Configurados

### Usuario: **jefe**
- Email: jefe@example.com
- Rol: JEFE
- Dashboard: `/dashboard-jefe/`

### Usuario: **encargado**  
- Email: encargado@example.com
- Rol: ENCARGADO
- Dashboard: `/dashboard-encargado/`

## Comandos Disponibles

### Listar todos los usuarios y sus roles
```bash
python manage.py listar_usuarios_roles
```

### Configurar un usuario como JEFE
```bash
python manage.py configurar_rol_jefe <username>
```

### Configurar un usuario como ENCARGADO
```bash
python manage.py configurar_rol_encargado <username>
```

## Cómo Probar

1. **Iniciar sesión como Jefe:**
   - Usuario: `jefe`
   - Contraseña: (la que configuraste)
   - Deberías ser redirigido a: `/dashboard-jefe/`

2. **Iniciar sesión como Encargado:**
   - Usuario: `encargado`
   - Contraseña: (la que configuraste)
   - Deberías ser redirigido a: `/dashboard-encargado/`

## Estructura de Redirección

Después del login, el sistema redirige según el rol:
- **JEFE** → Dashboard de Jefe
- **ENCARGADO** → Dashboard de Encargado
- **MECÁNICO** → Dashboard de Mecánico
- **Otros** → Página de inicio

## Notas Importantes

- Los campos de roles (`es_jefe`, `es_encargado`, `es_mecanico`) se agregaron al modelo `UserProfile`
- La migración `0011_userprofile_es_encargado_userprofile_es_jefe_and_more` ya fue aplicada
- Los usuarios existentes necesitan ser configurados manualmente con los comandos de gestión
