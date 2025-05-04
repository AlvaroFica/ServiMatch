from django.shortcuts import render
from django.http import JsonResponse

#Creación de views de usuarios

#Creacion de vista saludo
def saludo(request):
    return JsonResponse({'mensaje' : 'Hola estoy saludando desde la api backend' })

def vista_login(request):
    return render(request, 'login.html')

def vista_registrar_trabajador(request):
    return render(request, 'registrar-trabajador.html')
