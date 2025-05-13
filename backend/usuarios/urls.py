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
    MensajeViewSet,
    PlanServicioViewSet,
    ServicioViewSet
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
router.register(r'planeservicio', PlanServicioViewSet)


urlpatterns = [
    path('login/', views.vista_login, name='login'),
    path('', include(router.urls)),
    path('registrar-trabajador/', views.vista_registrar_trabajador, name='Registrar-trabajador'),
    path('usuario/<int:usuario_id>/', views.vista_usuario_detalle, name='detalle-usuario'),
    path('servicios/<int:pk>/imagenes/', ServicioViewSet.as_view({'post': 'subir_imagenes'}), name='servicio-subir-imagenes'),

    # rutas para los gráficos:
    path('graficos/usuarios-por-comuna/', views.api_usuarios_por_comuna),
    path('graficos/trabajadores-por-especialidad/', views.api_trabajadores_por_especialidad),
    path('graficos/servicios-mas-ofrecidos/', views.api_servicios_mas_ofrecidos),
    path('graficos/boletas-por-tipo-pago/', views.api_boletas_por_tipo_pago),
    path('graficos/monto-total-por-usuario/', views.api_monto_total_por_usuario),
]
