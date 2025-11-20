# Especificación de Requisitos de Software

**Proyecto:** Sistema de Gestión Integral para Talleres Mecánicos
**Versión:** 1.0
**Fecha:** 17 de noviembre de 2025
**Autores:** Christian Aguilar

## Introducción

### Propósito

Este documento presenta la especificación de requisitos de software para el Sistema de Gestión Integral de Talleres Mecánicos. El propósito es establecer de manera completa y detallada los requisitos funcionales y no funcionales del sistema, sirviendo como base contractual entre los desarrolladores y los interesados. El documento está dirigido a desarrolladores, personal técnico, administradores del taller y responsables de mantenimiento del sistema.

### Ámbito del sistema

El Sistema de Gestión Integral para Talleres Mecánicos es una aplicación web que permite la administración completa de operaciones en establecimientos dedicados al mantenimiento y reparación de vehículos. El sistema abarca la gestión de clientes, empleados, vehículos, servicios, reparaciones, citas y tareas del personal mediante dos roles diferenciados: Jefe y Encargado. La aplicación proporciona dashboards especializados, control de estados de reparación en tiempo real y generación de reportes de ingresos exportables.

### Definiciones, acrónimos y abreviaturas

**CRUD:** Create, Read, Update, Delete. Operaciones básicas de persistencia de datos.

**DRF:** Django REST Framework. Framework para construcción de APIs REST en Django.

**ORM:** Object-Relational Mapping. Técnica de conversión entre objetos y bases de datos relacionales.

**API REST:** Application Programming Interface basada en arquitectura RESTful.

**AJAX:** Asynchronous JavaScript and XML. Técnica de desarrollo web para aplicaciones asíncronas.

**WSGI:** Web Server Gateway Interface. Especificación estándar para servidores web Python.

**SQLite:** Sistema de gestión de bases de datos relacional embebido.

**MySQL:** Sistema de gestión de bases de datos relacional de código abierto.

### Referencias

Django Documentation 5.2. Disponible en: https://docs.djangoproject.com/

Django REST Framework Documentation 3.16. Disponible en: https://www.django-rest-framework.org/

IEEE Std 830-1998. Recommended Practice for Software Requirements Specifications.

Python Software Foundation. Python 3.11 Documentation. Disponible en: https://docs.python.org/3.11/

### Visión general del documento

Este documento está estructurado en tres secciones principales conforme al estándar IEEE 830. La segunda sección describe las características generales del sistema, incluyendo perspectiva del producto, funciones principales y características de usuarios. La tercera sección detalla los requisitos específicos funcionales, de interfaces externas, de rendimiento, restricciones de diseño y atributos del sistema. El documento emplea un enfoque técnico y conciso para facilitar su comprensión e implementación.

## Descripción General

### Perspectiva del producto

El sistema es una aplicación web independiente desarrollada con Django 5.2.8 que opera bajo arquitectura cliente-servidor mediante navegador web. Utiliza Django REST Framework para exponer una API RESTful que permite interacción con el frontend basado en templates HTML y JavaScript. El sistema se conecta a una base de datos relacional SQLite o MySQL para persistencia de datos y genera archivos Excel para exportación de reportes mediante bibliotecas especializadas.

### Funciones del producto

El sistema permite gestionar clientes mediante operaciones de registro, modificación, eliminación y búsqueda avanzada por múltiples criterios. Administra empleados del taller asignándoles puestos específicos y vinculándolos con perfiles de usuario del sistema. Registra vehículos asociados a clientes con información técnica completa y mantiene historial de servicios realizados. Controla el flujo completo de reparaciones desde ingreso hasta entrega, rastreando seis estados diferentes con validación de transiciones.

El sistema gestiona un catálogo de servicios con costos y duraciones estimadas, permitiendo agendamiento de citas con validación de conflictos horarios. Implementa un módulo de tareas para asignación y seguimiento de actividades del personal con prioridades y estados configurables. Proporciona dashboards especializados por rol con estadísticas, gráficos y métricas relevantes. Genera reportes de ingresos mensuales con capacidad de exportación a formato Excel para análisis financiero.

### Características de los usuarios

El sistema define dos tipos de usuarios principales con diferentes niveles de acceso y responsabilidades. Los usuarios con rol Jefe poseen acceso administrativo completo con capacidad de gestión CRUD sobre clientes, empleados y servicios. Tienen acceso a dashboards con métricas financieras, análisis de rendimiento y estadísticas globales del taller. Pueden configurar catálogo de servicios, precios y gestionar todas las operaciones del sistema sin restricciones.

Los usuarios con rol Encargado tienen acceso operacional limitado enfocado en actividades diarias del taller. Pueden gestionar citas, visualizar información de clientes y empleados, administrar vehículos y controlar tareas asignadas. Su dashboard presenta información relevante para operaciones diarias como citas del día, reparaciones en progreso y tareas pendientes. Ambos roles requieren conocimientos básicos de navegación web y comprensión de procesos operativos de talleres mecánicos.

### Restricciones

El sistema requiere Python 3.11 como entorno de ejecución obligatorio para compatibilidad con Django 5.2.8. Debe ejecutarse en servidores con soporte WSGI y opcionalmente ASGI para operaciones asíncronas. La base de datos debe ser SQLite para desarrollo o MySQL/MariaDB para entornos de producción, requiriendo mysqlclient 2.2.7 para conectividad. Los navegadores de usuario deben soportar JavaScript, CSS3 y HTML5 para correcta visualización de interfaces.

El sistema debe cumplir con las restricciones de seguridad de Django incluyendo protección CSRF, validación de entrada y autenticación basada en sesiones. Las operaciones de escritura requieren autenticación obligatoria y autorización basada en roles. La exportación de reportes está limitada por memoria disponible del servidor debido a procesamiento en memoria de archivos Excel. El sistema no implementa concurrencia optimista, por lo que actualizaciones simultáneas pueden presentar condiciones de carrera.

### Factores que se asumen y futuros requisitos

Se asume que el sistema operará en red local o con conexión estable a internet para acceso mediante navegador. Se presume que los usuarios recibirán capacitación básica sobre funcionalidades del sistema antes de uso productivo. Se considera que el volumen de datos no excederá 10,000 registros combinados en fase inicial, permitiendo uso de SQLite en desarrollo. Se asume disponibilidad de respaldos automáticos de base de datos mediante herramientas externas al sistema.

Como futuros requisitos se contempla implementación de notificaciones automáticas por email o SMS para recordatorios de citas. Se planea integración con sistemas de inventario para gestión de repuestos y materiales utilizados en reparaciones. Se prevé desarrollo de aplicación móvil para consulta de estado de reparaciones por parte de clientes. Se considera implementación de sistema de facturación electrónica integrado con autoridades fiscales y generación de módulo de análisis predictivo para mantenimiento preventivo basado en historial de vehículos.

## Requisitos Específicos

### Requisitos funcionales

#### Gestión de Autenticación y Autorización

El sistema debe proporcionar mecanismo de autenticación mediante usuario y contraseña validados contra base de datos. Debe mantener sesiones de usuario mediante cookies seguras con expiración configurable. Debe implementar dos roles de usuario diferenciados: Jefe con permisos administrativos completos y Encargado con permisos operacionales limitados. Debe restringir acceso a funcionalidades según rol asignado mediante decoradores de autorización.

#### Gestión de Clientes

El sistema debe permitir registro de clientes con información obligatoria de nombre, apellido, teléfono, dirección y correo electrónico único. Debe validar unicidad de correo electrónico rechazando duplicados. Debe permitir búsqueda de clientes por nombre, apellido, correo o teléfono mediante API REST. Usuarios con rol Jefe pueden crear, modificar y eliminar clientes mientras que Encargados pueden crear y modificar sin capacidad de eliminación.

#### Gestión de Empleados

El sistema debe permitir registro de empleados con nombre, puesto, teléfono y correo electrónico único. Debe vincular empleados con perfiles de usuario del sistema mediante relación uno a uno. Debe permitir asignación de puestos predefinidos como Jefe, Mecánico, Recepcionista. Solo usuarios con rol Jefe pueden gestionar información de empleados mediante operaciones CRUD completas.

#### Gestión de Vehículos

El sistema debe permitir registro de vehículos asociados a clientes con información de marca, modelo, año y placa única. Debe validar unicidad de placa rechazando duplicados en el sistema. Debe mantener relación de uno a muchos entre cliente y vehículos permitiendo múltiples vehículos por cliente. Debe permitir consulta de historial completo de reparaciones por vehículo.

#### Gestión de Servicios

El sistema debe mantener catálogo de servicios con nombre, descripción, costo y duración estimada en minutos. Solo usuarios con rol Jefe pueden crear, modificar o eliminar servicios del catálogo. Los servicios deben estar disponibles para selección en agendamiento de citas y registro de reparaciones.

#### Gestión de Reparaciones

El sistema debe registrar reparaciones vinculando vehículo, servicio, fechas de ingreso y salida. Debe implementar seis estados de reparación: pendiente, en progreso, en espera, revisión, completada y cancelada. Debe permitir transiciones de estado con actualización en tiempo real mediante interfaz web. Debe registrar condición del vehículo en cinco niveles: excelente, bueno, regular, malo, crítico. Debe permitir ingreso de notas adicionales en formato texto libre.

#### Gestión de Citas

El sistema debe permitir agendamiento de citas asociando cliente, servicio, fecha y hora. Debe validar que fecha y hora de cita no sean anteriores al momento actual. Debe prevenir agendamiento de citas en horarios ya ocupados mediante validación de conflictos. Debe proporcionar API para consulta de horarios disponibles en fecha específica.

#### Gestión de Tareas

El sistema debe permitir creación de tareas con título, descripción, prioridad y fecha límite. Debe soportar tres estados: por hacer, en progreso y completada. Debe permitir asignación de tareas a usuarios específicos del sistema. Debe permitir cambio de estado mediante interfaz AJAX sin recarga de página. Debe clasificar tareas en tres niveles de prioridad: baja, media y alta.

#### Dashboards Especializados

El sistema debe proporcionar dashboard para rol Jefe con estadísticas de clientes, empleados, servicios y vehículos totales. Debe incluir gráfico de reparaciones por estado y tabla de vehículos con más reparaciones en últimos treinta días. Debe mostrar análisis de ingresos mensuales de últimos seis meses y cantidad de clientes nuevos del mes actual.

El sistema debe proporcionar dashboard para rol Encargado con listado de citas programadas para día actual. Debe mostrar reparaciones en estado de progreso y próximas citas de siguientes siete días. Debe incluir resumen de tareas propias segmentadas por estado actual.

#### Generación de Reportes

El sistema debe generar reportes de ingresos mensuales calculando suma de costos de servicios por reparaciones completadas. Debe permitir exportación de reportes a formato Excel con formato tabular. Debe incluir en exportación columnas de mes, año, cantidad de servicios e ingreso total.

### Requisitos de interfaces externas

#### Interfaz de Usuario Web

El sistema debe proporcionar interfaz web responsive accesible mediante navegadores Chrome, Firefox, Safari y Edge en versiones recientes. Debe implementar formularios HTML con validación en cliente mediante JavaScript y validación en servidor mediante Django Forms. Debe utilizar templates Django para renderizado de vistas con separación de lógica de presentación.

#### API REST

El sistema debe exponer API REST mediante Django REST Framework en endpoints documentados. Debe soportar operaciones CRUD para recursos de clientes, empleados, servicios, vehículos, reparaciones y citas. Debe retornar respuestas en formato JSON con códigos HTTP estándar para operaciones exitosas y errores. Debe implementar serialización y deserialización de objetos mediante Django REST Framework Serializers.

#### Base de Datos

El sistema debe conectarse a base de datos SQLite mediante driver integrado en Python para entorno de desarrollo. Debe soportar conexión a MySQL o MariaDB mediante mysqlclient 2.2.7 para entorno de producción. Debe utilizar Django ORM para abstracción de operaciones de base de datos independiente del motor. Debe ejecutar migraciones de esquema mediante sistema de migraciones de Django.

#### Exportación de Archivos

El sistema debe generar archivos Excel en formato XLSX mediante bibliotecas openpyxl y xlsxwriter. Debe entregar archivos generados mediante respuesta HTTP con tipo MIME application/vnd.openxmlformats-officedocument.spreadsheetml.sheet. Los archivos generados deben ser compatibles con Microsoft Excel 2010 y versiones posteriores.

### Requisitos de rendimiento

El sistema debe responder a solicitudes de lectura de datos en tiempo máximo de dos segundos bajo carga normal. Las operaciones de escritura incluyendo creación y actualización deben completarse en máximo tres segundos. La generación de reportes Excel debe completarse en máximo cinco segundos para conjuntos de datos de hasta mil registros. El sistema debe soportar hasta cincuenta usuarios concurrentes sin degradación perceptible de rendimiento.

Las consultas a base de datos deben utilizar índices en campos de búsqueda frecuente como correo electrónico y placa de vehículo. El sistema debe implementar paginación en listados con más de cincuenta registros para optimizar transferencia de datos. Las operaciones AJAX de cambio de estado deben responder en menos de un segundo.

### Restricciones de diseño

El sistema debe implementar arquitectura Modelo-Vista-Template de Django manteniendo separación de responsabilidades. Debe utilizar Django ORM exclusivamente para acceso a datos evitando consultas SQL directas. Debe implementar autenticación mediante sistema de usuarios integrado de Django con extensión de perfil personalizado. Debe utilizar decoradores de Django para control de acceso basado en roles.

El sistema debe implementar protección CSRF en todos los formularios mediante tokens generados por Django. Debe validar datos de entrada en dos capas: cliente mediante JavaScript y servidor mediante Django Forms. Debe utilizar migraciones de Django para control de versiones de esquema de base de datos. El código debe seguir convenciones PEP 8 para estilo de código Python.

### Atributos del sistema

#### Seguridad

El sistema debe almacenar contraseñas mediante algoritmo de hash PBKDF2 con salt aleatorio implementado por Django. Debe implementar protección contra inyección SQL mediante uso exclusivo de Django ORM con consultas parametrizadas. Debe prevenir ataques XSS mediante escape automático de variables en templates Django. Debe implementar protección CSRF mediante tokens en formularios POST.

#### Mantenibilidad

El sistema debe incluir tests unitarios para modelos de datos validando restricciones y métodos personalizados. Debe documentar modelos, vistas y funciones principales mediante docstrings en formato reStructuredText. Debe mantener estructura modular con separación de aplicaciones Django por dominio funcional. El código debe seguir principio DRY evitando duplicación mediante reutilización de componentes.

#### Portabilidad

El sistema debe operar en sistemas operativos Linux, Windows y macOS sin modificaciones de código. Debe funcionar con Python 3.11 y versiones posteriores compatibles con Django 5.2.8. Debe soportar implementación mediante servidor WSGI estándar como Gunicorn o uWSGI. Debe permitir migración entre SQLite y MySQL mediante modificación de configuración sin cambios en código.

#### Usabilidad

El sistema debe proporcionar mensajes de error descriptivos en español para operaciones fallidas. Debe implementar validación de formularios con retroalimentación inmediata sobre campos inválidos. Debe utilizar código de colores y emojis para representación visual de estados de reparación. La navegación debe ser intuitiva con máximo tres clics para acceder a cualquier funcionalidad principal.

#### Confiabilidad

El sistema debe registrar errores y excepciones en logs para diagnóstico y auditoría. Debe implementar transacciones de base de datos para operaciones críticas garantizando consistencia. Debe validar integridad referencial mediante restricciones de clave foránea en nivel de base de datos. Debe manejar errores de conectividad con base de datos mediante excepciones apropiadas y mensajes al usuario.
