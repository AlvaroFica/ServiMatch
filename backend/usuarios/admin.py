from django.contrib import admin

# Register your models here.
from .models import (
    Pais, Region, Ciudad, Comuna, Usuario, Membresia,
    Especialidad, TipoEspecialidad, Trabajador, TipoServicio,
    Servicio, TipoPago, Boleta, Pago, Cita, Chat, Mensaje,
    PlanServicioTrabajador
)

admin.site.register(Pais)
admin.site.register(Region)
admin.site.register(Ciudad)
admin.site.register(Comuna)
admin.site.register(Usuario)
admin.site.register(Membresia)
admin.site.register(Especialidad)
admin.site.register(TipoEspecialidad)
admin.site.register(Trabajador)
admin.site.register(TipoServicio)
admin.site.register(Servicio)  # Registra el modelo Servicio
admin.site.register(TipoPago)
admin.site.register(Boleta)
admin.site.register(Pago)
admin.site.register(Cita)
admin.site.register(Chat)
admin.site.register(Mensaje)
admin.site.register(PlanServicioTrabajador)