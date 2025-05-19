from django.contrib import admin
from .models import TipoServicio

from .models import (
    Usuario,
    Especialidad,
    Trabajador,
    Servicio,
    ImagenServicio,
    PlanServicio,
)


@admin.register(TipoServicio)
class TipoServicioAdmin(admin.ModelAdmin):
    list_display  = ('id', 'nombre_tipo')
    search_fields = ('nombre_tipo',)

# Ya tenías esto:
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'rut', 'nombre', 'apellido', 'correo', 'telefono')
    search_fields = ('rut', 'nombre', 'apellido', 'correo')

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_esp')
    search_fields = ('nombre_esp',)

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'especialidad', 'estado_verificado', 'latitud', 'longitud')
    search_fields = ('usuario__nombre', 'usuario__apellido')

# AGREGAR esto para Servicio, ImagenServicio y PlanServicio:
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_serv', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nombre_serv', 'descripcion_breve')
    filter_horizontal = ('trabajadores',)   # para elegir varios trabajadores con widget

@admin.register(ImagenServicio)
class ImagenServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'servicio', 'imagen')

@admin.register(PlanServicio)
class PlanServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'servicio', 'nombre_plan', 'precio')
