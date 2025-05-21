from django.contrib import admin
from django.urls import path
from frontapp import views

urlpatterns = [
    path('', views.login, name='login'),
    path('registrar/', views.register, name='registrar-trabajador'),
    path('prueba/', views.prueba, name='prueba'),
    path('pagina_inicio/',views.vista_pagina_inicio, name='pagina_inicio'),
    path('cliente_inicio/', views.vista_cliente_inicio, name='cliente_inicio'),
    path('perfil_cliente/', views.perfil_cliente, name='perfil_cliente'),
    path('principal_pagina/', views.vista_principal_pagina, name='principal_pagina'),
    path('c_trabajador/', views.C_trabajador, name='c_trabajador'),
    path('introduccion_trab/', views.introduccion_trab, name='introduccion_trab'),
    path('registro_trabajador/', views.vista_registro_trabajador, name='registro_trabajador'),
    path('logout/', views.logout, name='logout'),
    path('perfil_trabajador/', views.vista_perfil_trabajador, name='perfil_trabajador'),
    path('perfil_trabajador/<int:usuario_id>/', views.vista_perfil_trabajador_id, name='perfil_trabajador_id'),
    path('mis_servicios/', views.vista_mis_servicios, name='mis_servicios'),
    path('agregar_servicio/', views.vista_agregar_servicio, name='agregar_servicio'),
    path('planes_servicio/<int:servicio_id>/',views.vista_ver_planes,name='ver_planes'),
    path('exito/', views.vista_mensaje_exito, name='mensaje_exito'),
    path('dashboard-admin/', views.vista_dashboard_admin, name='dashboard_admin'),
    path('admin/usuarios/', views.vista_admin_usuarios, name='admin_usuarios'),
    path('admin/trabajadores/', views.vista_admin_trabajadores, name='admin_trabajadores'),
    path('admin/servicios/', views.vista_admin_servicios, name='admin_servicios'),
    path('admin/boletas/', views.vista_admin_boletas, name='admin_boletas'),
    path('dashboard-admin/pendientes/', views.vista_admin_pendientes, name='admin_pendientes'),
    path('admin/cpu_admin', views.cpu_admin, name='cpu_admin'),
    path('admin/acciones', views.acciones, name='acciones'),
    path('planes_servicio/<int:servicio_id>/crear/',views.vista_crear_plan,name='crear_plan'),
    path('contratar/<int:plan_id>/', views.vista_contratar, name='contratar'),
    path('chat/<int:chat_id>/',   views.vista_chat,      name='chat'),
]
