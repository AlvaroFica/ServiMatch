from django.core.management.base import BaseCommand
from usuarios.models import *
from django.contrib.auth.hashers import make_password
from datetime import date
import random
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = 'Carga datos demo completos con Chile completo (regiones, ciudades, comunas, especialidades, usuarios, trabajadores y servicios).'

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

        # ===== Regiones, ciudades, comunas Chile =====
        regiones_data = [
    {"nombre": "Región de Arica y Parinacota", "ciudades": [{"nombre": "Arica", "comunas": ["Arica", "Camarones"]}, {"nombre": "Putre", "comunas": ["Putre", "General Lagos"]}]},
    {"nombre": "Región de Tarapacá", "ciudades": [{"nombre": "Iquique", "comunas": ["Iquique", "Alto Hospicio"]}, {"nombre": "Tamarugal", "comunas": ["Pozo Almonte", "Pica", "Huara", "Camiña", "Colchane"]}]},
    {"nombre": "Región de Antofagasta", "ciudades": [{"nombre": "Antofagasta", "comunas": ["Antofagasta", "Mejillones", "Sierra Gorda", "Taltal"]}, {"nombre": "Calama", "comunas": ["Calama", "San Pedro de Atacama", "Ollagüe"]}, {"nombre": "Tocopilla", "comunas": ["Tocopilla", "María Elena"]}]},
    {"nombre": "Región de Atacama", "ciudades": [{"nombre": "Copiapó", "comunas": ["Copiapó", "Caldera", "Tierra Amarilla"]}, {"nombre": "Vallenar", "comunas": ["Vallenar", "Huasco", "Alto del Carmen", "Freirina"]}, {"nombre": "Chañaral", "comunas": ["Chañaral", "Diego de Almagro"]}]},
    {"nombre": "Región de Coquimbo", "ciudades": [{"nombre": "La Serena", "comunas": ["La Serena", "Coquimbo"]}, {"nombre": "Ovalle", "comunas": ["Ovalle", "Monte Patria", "Combarbalá", "Punitaqui", "Río Hurtado"]}, {"nombre": "Illapel", "comunas": ["Illapel", "Salamanca", "Los Vilos", "Canela"]}]},
    {"nombre": "Región de Valparaíso", "ciudades": [{"nombre": "Valparaíso", "comunas": ["Valparaíso", "Viña del Mar", "Concón", "Quintero", "Puchuncaví"]}, {"nombre": "San Antonio", "comunas": ["San Antonio", "Cartagena", "El Tabo", "El Quisco", "Algarrobo"]}, {"nombre": "Quillota", "comunas": ["Quillota", "La Calera", "La Cruz", "Nogales", "Hijuelas"]}, {"nombre": "Los Andes", "comunas": ["Los Andes", "San Felipe", "Llaillay", "Panquehue", "Santa María"]}, {"nombre": "Isla de Pascua", "comunas": ["Isla de Pascua"]}]},
    {"nombre": "Región Metropolitana", "ciudades": [{"nombre": "Santiago", "comunas": ["Santiago", "Providencia", "Las Condes", "Ñuñoa", "La Florida", "San Bernardo", "Maipú", "Puente Alto", "Pudahuel", "Cerro Navia", "Quilicura", "Renca", "Independencia", "Estación Central", "La Reina", "Peñalolén", "Lo Barnechea", "Huechuraba", "Pedro Aguirre Cerda", "San Joaquín", "Macul", "La Granja", "San Ramón", "La Cisterna", "El Bosque", "Lo Espejo", "La Pintana", "Padre Hurtado", "Melipilla", "Talagante", "Buin", "Paine", "Colina", "Lampa", "Til Til"]}]},
    {"nombre": "Región del Libertador General Bernardo O'Higgins", "ciudades": [{"nombre": "Rancagua", "comunas": ["Rancagua", "Machalí", "Graneros", "Mostazal", "Codegua", "Doñihue", "Requínoa", "Rengo", "Malloa", "San Vicente", "Peumo", "Las Cabras", "Pichidegua", "Chimbarongo", "Santa Cruz", "Paredones", "Peralillo", "Palmilla", "Lolol", "Marchigüe"]}]},
    {"nombre": "Región del Maule", "ciudades": [{"nombre": "Talca", "comunas": ["Talca", "San Clemente", "Pelarco", "Pencahue", "Maule", "San Rafael"]}, {"nombre": "Curicó", "comunas": ["Curicó", "Teno", "Romeral", "Sagrada Familia", "Hualañé", "Licantén", "Vichuquén"]}, {"nombre": "Linares", "comunas": ["Linares", "San Javier", "Yerbas Buenas", "Colbún", "Villa Alegre", "Longaví", "Retiro", "Parral", "Cauquenes", "Chanco", "Pelluhue"]}]},
    {"nombre": "Región del Ñuble", "ciudades": [{"nombre": "Chillán", "comunas": ["Chillán", "Chillán Viejo", "Bulnes", "Quillón", "Yungay", "El Carmen", "San Ignacio", "Pinto", "Coihueco", "San Carlos", "Ninhue", "San Fabián", "Trehuaco", "Quirihue", "Cobquecura", "Portezuelo", "Ránquil"]}]},
    {"nombre": "Región del Biobío", "ciudades": [{"nombre": "Concepción", "comunas": ["Concepción", "Talcahuano", "San Pedro de la Paz", "Chiguayante", "Hualpén", "Coronel", "Lota", "Penco", "Tomé", "Florida", "Hualqui", "Santa Juana"]}, {"nombre": "Los Ángeles", "comunas": ["Los Ángeles", "Nacimiento", "Laja", "San Rosendo", "Santa Bárbara", "Quilleco", "Tucapel", "Antuco", "Mulchén", "Collipulli", "Curanilahue", "Cañete", "Contulmo", "Tirúa", "Arauco", "Lebu"]}]},
    {"nombre": "Región de La Araucanía", "ciudades": [{"nombre": "Temuco", "comunas": ["Temuco", "Padre Las Casas", "Nueva Imperial", "Carahue", "Cholchol", "Cunco", "Curarrehue", "Freire", "Gorbea", "Lautaro", "Loncoche", "Melipeuco", "Perquenco", "Pitrufquén", "Pucón", "Saavedra", "Teodoro Schmidt", "Toltén", "Vilcún", "Villarrica", "Angol", "Collipulli", "Curacautín", "Ercilla", "Lonquimay", "Los Sauces", "Lumaco", "Purén", "Renaico", "Traiguén", "Victoria"]}]},
    {"nombre": "Región de Los Ríos", "ciudades": [{"nombre": "Valdivia", "comunas": ["Valdivia", "Corral", "Mariquina", "Lanco", "Máfil", "Los Lagos", "Panguipulli"]}, {"nombre": "La Unión", "comunas": ["La Unión", "Río Bueno", "Futrono", "Lago Ranco"]}]},
    {"nombre": "Región de Los Lagos", "ciudades": [{"nombre": "Puerto Montt", "comunas": ["Puerto Montt", "Puerto Varas", "Frutillar", "Llanquihue", "Calbuco", "Cochamó", "Maullín"]}, {"nombre": "Osorno", "comunas": ["Osorno", "Río Negro", "Purranque", "Puyehue", "San Pablo"]}, {"nombre": "Castro", "comunas": ["Castro", "Ancud", "Chonchi", "Dalcahue", "Curaco de Vélez", "Quinchao", "Quellón", "Quemchi"]}]},
    {"nombre": "Región de Aysén del General Carlos Ibáñez del Campo", "ciudades": [{"nombre": "Coyhaique", "comunas": ["Coyhaique", "Lago Verde"]}, {"nombre": "Aysén", "comunas": ["Aysén", "Cisnes", "Guaitecas"]}, {"nombre": "Cochrane", "comunas": ["Cochrane", "O'Higgins", "Tortel"]}]},
    {"nombre": "Región de Magallanes y de la Antártica Chilena", "ciudades": [{"nombre": "Punta Arenas", "comunas": ["Punta Arenas", "Río Verde", "Laguna Blanca", "San Gregorio"]}, {"nombre": "Puerto Natales", "comunas": ["Natales", "Torres del Paine"]}, {"nombre": "Porvenir", "comunas": ["Porvenir", "Primavera", "Timaukel"]}, {"nombre": "Antártica", "comunas": ["Antártica"]}]}
]


        comunas_cargadas = []

        for r in regiones_data:
            region = Region.objects.create(nombre_region=r["nombre"], pais=pais)
            for c in r["ciudades"]:
                ciudad = Ciudad.objects.create(nombre_ciudad=c["nombre"], region=region)
                for com in c["comunas"]:
                    comuna = Comuna.objects.create(nombre_comuna=com, ciudad=ciudad)
                    comunas_cargadas.append(comuna)

        # ===== Especialidades =====
        especialidades = [
            "Gasfiter",
            "Electricista",
            "Carpintero",
            "Pintor",
            "Cerrajero",
            "Jardinero",
            "Albañil",
            "Técnico en refrigeración",
            "Técnico en aire acondicionado",
            "Mecánico automotriz",
            "Mecánico de bicicletas",
            "Técnico en electrodomésticos",
            "Yesero",
            "Soldador",
            "Techador",
            "Maestro de obras",
            "Instalador de pisos",
            "Instalador de ventanas y vidrios",
            "Instalador de puertas",
            "Instalador de cortinas y persianas",
            "Tapicero",
            "Herrero",
            "Paisajista",
            "Podador de árboles",
            "Mantenimiento de piscinas",
            "Personal de aseo domiciliario",
            "Personal de aseo industrial",
            "Limpieza de vidrios en altura",
            "Lavado de alfombras y tapices",
            "Flete y mudanza",
            "Chofer particular",
            "Motoboy / Delivery independiente",
            "Instalador de sistemas de riego",
            "Técnico en calefacción",
            "Técnico en paneles solares",
            "Instalador de sistemas de seguridad",
            "Instalador de antenas y TV cable",
            "Técnico en computación",
            "Desabollador y pintor automotriz"
        ]

        especialidades_objs = [Especialidad.objects.create(nombre_esp=e) for e in especialidades]

        tipo1 = TipoServicio.objects.create(nombre_tipo="Reparación")
        tipo2 = TipoServicio.objects.create(nombre_tipo="Instalación")
        pago1 = TipoPago.objects.create(descripcion="Efectivo")
        pago2 = TipoPago.objects.create(descripcion="Transferencia")

        fake_image = ContentFile(b"fake image data", name='fake.jpg')

        usuarios = []
        trabajadores = []

        for i in range(30):
            comuna_aleatoria = random.choice(comunas_cargadas)
            u = Usuario.objects.create(
                rut=f"1234567{i}-K",
                nombre=f"Trabajador{i}",
                apellido="Demo",
                correo=f"trabajador{i}@mail.com",
                telefono="912345678",
                fecha_nac=date(1990, 1, (i % 28) + 1),
                comuna=comuna_aleatoria,
                contraseña=make_password("1234"),
                foto_perfil=fake_image
            )
            usuarios.append(u)

            t = Trabajador.objects.create(
                usuario=u,
                especialidad=random.choice(especialidades_objs),
                estado_verificado=True,
                foto_cedula=fake_image,
                foto_cedula_atras=fake_image,
                foto_autoretrato=fake_image,
                latitud=-33.45 + random.uniform(-2.0, 2.0),
                longitud=-70.66 + random.uniform(-2.0, 2.0)
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
            s.trabajadores.set(random.sample(trabajadores, k=random.randint(5, 10)))
            servicios.append(s)

            PlanServicio.objects.create(
                servicio=s,
                nombre_plan="Plan Básico",
                precio=random.randint(20000, 60000),
                duracion="1 día",
                incluye="Materiales básicos\nMano de obra\nGarantía 3 meses",
                descripcion_breve="Ideal para tareas pequeñas"
            )

        for _ in range(50):
            Boleta.objects.create(
                servicio=random.choice(servicios),
                usuario=random.choice(usuarios),
                monto=random.randint(20000, 80000),
                tipo_pago=random.choice([pago1, pago2])
            )

        print("✅ Datos demo cargados correctamente con Chile completo (regiones, ciudades, comunas, especialidades, usuarios y servicios).")
