from django.db import models

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



class Membresia(models.Model):
    nombre_membresia = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_membresia

class Especialidad(models.Model):
    nombre_esp = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_esp

class TipoEspecialidad(models.Model):
    nombre_tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_tipo

class Trabajador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_NULL, null=True)
    estado_verificado = models.BooleanField(default=False)
    foto_cedula = models.ImageField(upload_to='cedulas/')
    foto_cedula_atras = models.ImageField(upload_to='cedulas/')
    foto_autoretrato = models.ImageField(upload_to='selfies/')

    def __str__(self):
        return f"Trabajador: {self.usuario.nombre} {self.usuario.apellido}"

class TipoServicio(models.Model):
    nombre_tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_tipo

class Servicio(models.Model):
    nombre_serv = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoServicio, on_delete=models.SET_NULL, null=True)
    trabajadores = models.ManyToManyField('Trabajador', related_name='servicios', blank=True)

    def __str__(self):
        return self.nombre_serv

class TipoPago(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion

class Boleta(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_pago = models.ForeignKey(TipoPago, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Boleta de {self.usuario.nombre} - ${self.monto}"

class Pago(models.Model):
    pass  # Solo tiene ID

    def __str__(self):
        return f"Pago #{self.id}"

class Cita(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cita de {self.usuario.nombre} el {self.fecha_creacion.strftime('%Y-%m-%d')}"

class Chat(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    termino = models.TextField()

    def __str__(self):
        return f"Chat de la cita #{self.cita.id}"

class Mensaje(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    mensaje = models.TextField()

    def __str__(self):
        return f"Mensaje en chat #{self.chat.id}"
