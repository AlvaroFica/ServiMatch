from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Importar las vistas necesarias
from .views import (
    PaisViewSet,
    RegionViewSet,
    CiudadViewSet,
    ComunaViewSet,
    UsuarioViewSet,
    MembresiaViewSet,
    EspecialidadViewSet,
    TipoEspecialidadViewSet,
    TrabajadorViewSet,
    TipoServicioViewSet,
    ServicioViewSet,
    TipoPagoViewSet,
    BoletaViewSet,
    PagoViewSet,
    CitaViewSet,
    ChatViewSet,
    MensajeViewSet
)

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
    path('login/', views.vista_login, name='login'),
    path('', include(router.urls)),
    path('registrar-trabajador/', views.vista_registrar_trabajador, name='Registrar-trabajador'),
    path('usuario/<int:usuario_id>/', views.vista_usuario_detalle, name='detalle-usuario'),

]
