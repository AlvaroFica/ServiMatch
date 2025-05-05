from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'paises', PaisViewSet)
router.register(r'regiones', RegionViewSet)
router.register(r'ciudades', CiudadViewSet)
router.register(r'comunas', ComunaViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'membresias', MembresiaViewSet)
router.register(r'especialidades', EspecialidadViewSet)
router.register(r'tipoespecialidades', TipoEspecialidadViewSet)
router.register(r'trabajadores', TrabajadorViewSet)
router.register(r'tiposervicios', TipoServicioViewSet)
router.register(r'servicios', ServicioViewSet)
router.register(r'tipopagos', TipoPagoViewSet)
router.register(r'boletas', BoletaViewSet)
router.register(r'pagos', PagoViewSet)
router.register(r'citas', CitaViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'mensajes', MensajeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
