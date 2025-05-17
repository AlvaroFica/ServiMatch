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
    ServicioViewSet,
    api_monitor_uptime,
    api_monitor_errors,
    api_users_active_new,
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
    path('monitor/system-metrics/', views.api_system_metrics, name='monitor_system_metrics'),
    path('feedback/', views.api_feedback, name='api_feedback'),
    path('monitor/uptime/', api_monitor_uptime, name='monitor_uptime'),
    path('monitor/errors/', api_monitor_errors, name='monitor_errors'),
    path('monitor/users/', api_users_active_new, name='monitor_users'),
    path('login/', views.vista_login, name='login'),
    path('', include(router.urls)),
    path('registrar-trabajador/', views.vista_registrar_trabajador, name='Registrar-trabajador'),
    path('usuario/<int:usuario_id>/', views.vista_usuario_detalle, name='detalle-usuario'),
    path('servicios/<int:pk>/imagenes/', ServicioViewSet.as_view({'post': 'subir_imagenes'}), name='servicio-subir-imagenes'),

    path('monitor/logs/', views.api_audit_logs, name='monitor_logs'),
    # rutas para los gráficos:
    path('graficos/usuarios-por-comuna/', views.api_usuarios_por_comuna),
    path('graficos/trabajadores-por-especialidad/', views.api_trabajadores_por_especialidad),
    path('graficos/servicios-mas-ofrecidos/', views.api_servicios_mas_ofrecidos),
    path('graficos/boletas-por-tipo-pago/', views.api_boletas_por_tipo_pago),
    path('graficos/monto-total-por-usuario/', views.api_monto_total_por_usuario),
    path('graficos/total-usuarios/', views.api_total_usuarios),
    path('graficos/total-trabajadores/', views.api_total_trabajadores),
    path('graficos/total-servicios/', views.api_total_servicios),
    path('graficos/citas-este-mes/', views.api_citas_este_mes),
    path('graficos/trabajadores-pendientes/', views.api_trabajadores_pendientes),
    path('graficos/usuarios-online/', views.api_usuarios_online),
    path('admin/pendientes/', views.vista_admin_pendientes, name='admin_pendientes'),
]
