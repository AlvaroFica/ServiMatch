from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.vista_login, name='login'),
    path('registrar-trabajador/', views.vista_registrar_trabajador, name='Registrar-trabajador')
]