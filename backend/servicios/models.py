from django.db import models
from usuarios.models import Usuario

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    # …tus campos…

class Calificacion(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='calificaciones')
    cliente  = models.ForeignKey(Usuario,   on_delete=models.CASCADE, related_name='calificaciones')
    # …resto de campos…
