from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete

class UsuariosConfig(AppConfig):
    name = 'usuarios'

    def ready(self):
        from .models import AuditLog, Usuario, Trabajador, Servicio, Boleta, Cita
        from django.contrib.auth import get_user_model

        def log_action(sender, instance, created, **kwargs):
            AuditLog.objects.create(
                usuario    = getattr(instance, 'usuario', None),
                accion     = 'CREADO' if created else 'MODIFICADO',
                modelo     = sender.__name__,
                objeto_id  = instance.pk,
                detalle    = str(instance),   # ← aquí
            )

        def log_delete(sender, instance, **kwargs):
            AuditLog.objects.create(
                usuario    = getattr(instance, 'usuario', None),
                accion     = 'BORRADO',
                modelo     = sender.__name__,
                objeto_id  = instance.pk,
                detalle    = str(instance),   # ← y aquí
            )


        for model in (Usuario, Trabajador, Servicio, Boleta, Cita):
            post_save.connect(log_action, sender=model)
            post_delete.connect(log_delete, sender=model)