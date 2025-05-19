from django.db import models
from django.conf import settings  # ← necesario para AUTH_USER_MODEL

class TipoServicio(models.Model):
    nombre_tipo = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre_tipo

class Servicio(models.Model):
    nombre_serv = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoServicio, on_delete=models.SET_NULL, null=True)
    trabajadores = models.ManyToManyField('Trabajador', related_name='servicios', blank=True)
    descripcion_breve = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre_serv

class ImagenServicio(models.Model):
    servicio = models.ForeignKey(Servicio, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='servicios/imagenes/')

    def __str__(self):
        return f"Imagen de {self.servicio.nombre_serv}"

class PlanServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='planes')
    nombre_plan = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion = models.CharField(max_length=50)
    incluye = models.TextField()
    descripcion_breve = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre_plan} - ${self.precio}"

class Pais(models.Model):
    nombre_pais = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre_pais

class Region(models.Model):
    nombre_region = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre_region

class Ciudad(models.Model):
    nombre_ciudad = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre_ciudad

class Comuna(models.Model):
    nombre_comuna = models.CharField(max_length=100)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre_comuna

class Usuario(models.Model):
    rut = models.CharField(max_length=15, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_nac = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True)
    contraseña = models.CharField(max_length=255)
    foto_perfil = models.ImageField(upload_to='usuarios/fotos_perfil/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.correo})"

    @property
    def es_trabajador(self):
        return hasattr(self, 'trabajador')

class Especialidad(models.Model):
    nombre_esp = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre_esp

class Trabajador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_NULL, null=True)
    estado_verificado = models.BooleanField(default=False)
    foto_cedula = models.ImageField(upload_to='cedulas/')
    foto_cedula_atras = models.ImageField(upload_to='cedulas/')
    foto_autoretrato = models.ImageField(upload_to='selfies/')
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"Trabajador: {self.usuario.nombre} {self.usuario.apellido}"

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.nombre

class CalificacionEtiqueta(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='calificaciones')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    etiquetas = models.ManyToManyField(Etiqueta)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('servicio', 'usuario')

    def __str__(self):
        return f"Calificación de {self.usuario} a {self.servicio}"
