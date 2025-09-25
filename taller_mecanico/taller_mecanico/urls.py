"""
URL configuration for taller_mecanico project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from gestion.views import clientes_lista, inicio


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('gestion.urls')),  # Ruta base para la API

    # Rutas para las vistas basadas en plantillas
    path('', inicio, name='inicio'),
    path('clientes/lista/', clientes_lista, name='clientes-lista'),
    path('empleados/lista/', render, {'template_name': 'empleados_lista.html'}, name='empleados-lista'),
    path('servicios/lista/', render, {'template_name': 'servicios_lista.html'}, name='servicios-lista'),
]
