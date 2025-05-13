from django.core.management.base import BaseCommand
from usuarios.models import *
from django.contrib.auth.hashers import make_password
from datetime import date
import random
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = 'Carga datos demo para todos los modelos'

    def handle(self, *args, **kwargs):
        print("Borrando datos existentes...")
        Boleta.objects.all().delete()
        Servicio.objects.all().delete()
        Trabajador.objects.all().delete()
        Usuario.objects.all().delete()
        Comuna.objects.all().delete()
        Ciudad.objects.all().delete()
        Region.objects.all().delete()
        Pais.objects.all().delete()
        Especialidad.objects.all().delete()
        TipoServicio.objects.all().delete()
        TipoPago.objects.all().delete()
        PlanServicio.objects.all().delete()

        print("Creando registros nuevos...")

        pais = Pais.objects.create(nombre_pais="Chile")
        region = Region.objects.create(nombre_region="Metropolitana", pais=pais)
        ciudad = Ciudad.objects.create(nombre_ciudad="Santiago", region=region)
        comuna = Comuna.objects.create(nombre_comuna="San Bernardo", ciudad=ciudad)

        esp1 = Especialidad.objects.create(nombre_esp="Albañil")
        esp2 = Especialidad.objects.create(nombre_esp="Electricista")
        tipo1 = TipoServicio.objects.create(nombre_tipo="Reparación")
        tipo2 = TipoServicio.objects.create(nombre_tipo="Instalación")
        pago1 = TipoPago.objects.create(descripcion="Efectivo")
        pago2 = TipoPago.objects.create(descripcion="Transferencia")

        fake_image = ContentFile(b"fake image data", name='fake.jpg')

        usuarios = []
        trabajadores = []

        for i in range(5):
            u = Usuario.objects.create(
                rut=f"1234567{i}-K",
                nombre=f"Juan{i}",
                apellido="Pérez",
                correo=f"juan{i}@mail.com",
                telefono="912345678",
                fecha_nac=date(1990, 1, i+1),
                comuna=comuna,
                contraseña=make_password("1234"),
                foto_perfil=fake_image
            )
            usuarios.append(u)

            t = Trabajador.objects.create(
                usuario=u,
                especialidad=random.choice([esp1, esp2]),
                estado_verificado=True,
                foto_cedula=fake_image,
                foto_cedula_atras=fake_image,
                foto_autoretrato=fake_image
            )
            trabajadores.append(t)

        servicio_nombres = [
            "Instalación de luces",
            "Reparación de enchufes",
            "Arreglo de cañerías",
            "Pintura interior",
            "Cambio de cerámicas",
            "Instalación de muebles",
            "Servicio de gasfitería",
            "Mantenimiento eléctrico",
            "Revisión de calefacción",
            "Construcción de terraza"
        ]

        servicios = []
        for nombre in servicio_nombres:
            s = Servicio.objects.create(
                nombre_serv=nombre,
                tipo=random.choice([tipo1, tipo2]),
                descripcion_breve="Servicio profesional realizado con calidad garantizada."
            )
            s.trabajadores.set(random.sample(trabajadores, k=random.randint(1, 3)))
            servicios.append(s)

            # Plan de ejemplo
            PlanServicio.objects.create(
                servicio=s,
                nombre_plan="Plan Básico",
                precio=random.randint(20000, 60000),
                duracion="1 día",
                incluye="Materiales básicos\nMano de obra\nGarantía 3 meses",
                descripcion_breve="Ideal para tareas pequeñas"
            )

        for _ in range(10):
            Boleta.objects.create(
                servicio=random.choice(servicios),
                usuario=random.choice(usuarios),
                monto=random.randint(20000, 80000),
                tipo_pago=random.choice([pago1, pago2])
            )

        print("✅ Datos demo cargados correctamente.")
