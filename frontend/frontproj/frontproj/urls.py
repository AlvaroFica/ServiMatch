from django.contrib import admin
from django.urls import path
from frontapp import views

urlpatterns = [
    path('', views.login, name='login'),
    path('registrar/', views.register, name='registrar-trabajador'),
    path('prueba/', views.prueba, name='prueba'),
    path('pagina_inicio/',views.vista_pagina_inicio, name='pagina_inicio'),
    path('cliente_inicio/', views.vista_cliente_inicio, name='cliente_inicio'),
    path('trabajador_inicio/', views.vista_trabajador_inicio, name='trabajador_inicio'),
    path('perfil/', views.vista_perfil, name='perfil'),
    path('principal_pagina/', views.vista_principal_pagina, name='principal_pagina'),
    path('c_trabajador/', views.C_trabajador, name='c_trabajador'),
    path('introduccion_trab/', views.introduccion_trab, name='introduccion_trab'),
]
