from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CrearPlanServicioTrabajadorForm
from django.http import JsonResponse
from .models import *
from .serializers import *
from rest_framework import viewsets
from django.contrib import messages

#Creación de views de usuarios

#Creacion de vista saludo
def saludo(request):
    return JsonResponse({'mensaje' : 'Hola estoy saludando desde la api backend' })

def vista_login(request):
    return render(request, 'login.html')

def vista_registrar_trabajador(request):
    return render(request, 'registrar-trabajador.html')

@login_required
def crear_plan_servicio_trabajador(request):
    try:
        trabajador = Trabajador.objects.get(usuario=request.user)
    except Trabajador.DoesNotExist:
        messages.error(request, 'Tu perfil de trabajador no está completo.')
        return redirect('login') # Redirige a donde corresponda

    if request.method == 'POST':
        form = CrearPlanServicioTrabajadorForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.trabajador = trabajador
            try:
                plan.save()
                messages.success(request, 'El plan de servicio se ha creado exitosamente.')
                return redirect('nombre_de_tu_vista_de_listado_planes_trabajador') # Redirige a la lista de planes del trabajador
            except Exception as e:
                messages.error(request, f'Hubo un error al guardar el plan: {e}')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = CrearPlanServicioTrabajadorForm()

    return render(request, 'servicios/crear_plan_servicio_trabajador.html', {'form': form})

@login_required
def listar_planes_servicio_trabajador(request):
    try:
        trabajador = Trabajador.objects.get(usuario=request.user)
        planes = PlanServicioTrabajador.objects.filter(trabajador=trabajador).select_related('servicio')
        return render(request, 'servicios/listar_planes_trabajador.html', {'planes': planes})
    except Trabajador.DoesNotExist:
        messages.error(request, 'Tu perfil de trabajador no está completo.')
        return redirect('nombre_de_alguna_vista_de_perfil')

class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class CiudadViewSet(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer

class ComunaViewSet(viewsets.ModelViewSet):
    queryset = Comuna.objects.all()
    serializer_class = ComunaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class MembresiaViewSet(viewsets.ModelViewSet):
    queryset = Membresia.objects.all()
    serializer_class = MembresiaSerializer

class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer

class TipoEspecialidadViewSet(viewsets.ModelViewSet):
    queryset = TipoEspecialidad.objects.all()
    serializer_class = TipoEspecialidadSerializer

class TrabajadorViewSet(viewsets.ModelViewSet):
    queryset = Trabajador.objects.all()
    serializer_class = TrabajadorSerializer


class TipoServicioViewSet(viewsets.ModelViewSet):
    queryset = TipoServicio.objects.all()
    serializer_class = TipoServicioSerializer

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class TipoPagoViewSet(viewsets.ModelViewSet):
    queryset = TipoPago.objects.all()
    serializer_class = TipoPagoSerializer

class BoletaViewSet(viewsets.ModelViewSet):
    queryset = Boleta.objects.all()
    serializer_class = BoletaSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class MensajeViewSet(viewsets.ModelViewSet):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer
