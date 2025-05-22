from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'paises', views.PaisViewSet)
router.register(r'regiones', views.RegionViewSet)
router.register(r'ciudades', views.CiudadViewSet)
router.register(r'comunas', views.ComunaViewSet)
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'membresias', views.MembresiaViewSet)
router.register(r'especialidades', views.EspecialidadViewSet)
router.register(r'tipoespecialidades', views.TipoEspecialidadViewSet)
router.register(r'trabajadores', views.TrabajadorViewSet)
router.register(r'tiposervicios', views.TipoServicioViewSet)
router.register(r'servicios', views.ServicioViewSet)
router.register(r'tipopagos', views.TipoPagoViewSet)
router.register(r'boletas', views.BoletaViewSet)
router.register(r'pagos', views.PagoViewSet)
router.register(r'citas', views.CitaViewSet)
router.register(r'chats', views.ChatViewSet)
router.register(r'mensajes', views.MensajeViewSet)
router.register(r'planeservicio', views.PlanServicioViewSet)

urlpatterns = [
    # ---- monitor y auth ----
    path('monitor/system-metrics/', views.api_system_metrics,   name='monitor_system_metrics'),
    path('monitor/uptime/',          views.api_monitor_uptime,   name='monitor_uptime'),
    path('monitor/errors/',          views.api_monitor_errors,    name='monitor_errors'),
    path('monitor/users/',           views.api_users_active_new,  name='monitor_users'),
    path('monitor/logs/',            views.api_audit_logs,        name='monitor_logs'),
    path('login/',                   views.vista_login,           name='login'),

    # ---- API REST ----
    path('', include(router.urls)),
    path('feedback/',                views.api_feedback,          name='api_feedback'),
    path('chats-usuario/<int:usuario_id>/', views.api_chats_usuario, name='api_chats_usuario'),
    path('servicios/<int:pk>/imagenes/', views.ServicioViewSet.as_view({'post': 'subir_imagenes'}), name='servicio-subir-imagenes'),
    path('mercadopago/preferencia/', views.crear_preferencia_mp,   name='crear_preferencia_mp'),

    # ---- gráficos ----
    path('graficos/usuarios-por-comuna/',          views.api_usuarios_por_comuna,         name='graf_usuarios_por_comuna'),
    path('graficos/trabajadores-por-especialidad/',views.api_trabajadores_por_especialidad, name='graf_trabajadores_por_especialidad'),
    path('graficos/servicios-mas-ofrecidos/',      views.api_servicios_mas_ofrecidos,     name='graf_servicios_mas_ofrecidos'),
    path('graficos/boletas-por-tipo-pago/',        views.api_boletas_por_tipo_pago,       name='graf_boletas_por_tipo_pago'),
    path('graficos/monto-total-por-usuario/',      views.api_monto_total_por_usuario,     name='graf_monto_total_por_usuario'),
    path('graficos/total-usuarios/',               views.api_total_usuarios,              name='graf_total_usuarios'),
    path('graficos/total-trabajadores/',           views.api_total_trabajadores,          name='graf_total_trabajadores'),
    path('graficos/total-servicios/',              views.api_total_servicios,             name='graf_total_servicios'),
    path('graficos/citas-este-mes/',               views.api_citas_este_mes,              name='graf_citas_este_mes'),
    path('graficos/trabajadores-pendientes/',      views.api_trabajadores_pendientes,     name='graf_trabajadores_pendientes'),
    path('graficos/usuarios-online/',              views.api_usuarios_online,             name='graf_usuarios_online'),

    # ---- vistas front ----
    path('registrar-trabajador/', views.vista_registrar_trabajador, name='registrar_trabajador'),
    path('usuario/<int:usuario_id>/', views.vista_usuario_detalle,    name='detalle_usuario'),

    path('admin/citas/<int:cita_id>/toggle/', views.admin_cita_toggle, name='admin_cita_toggle'),

]
