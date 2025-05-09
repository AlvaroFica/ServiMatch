import requests
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        data = {
            'rut': request.POST.get('rut'),
            'nombre': request.POST.get('nombre'),
            'apellido': request.POST.get('apellido'),
            'correo': request.POST.get('correo'),
            'telefono': request.POST.get('celular'),
            'fecha_nac': request.POST.get('fecha_nacimiento'),
            'comuna': request.POST.get('comuna'),
            'contraseña': request.POST.get('contraseña'),
        }

        files = {}
        if 'foto_perfil' in request.FILES:
            files['foto_perfil'] = request.FILES['foto_perfil']

        try:
            response = requests.post('http://127.0.0.1:8000/api/usuarios/', data=data, files=files)
            if response.status_code == 201:
                return redirect('login')
            else:
                comunas = get_comunas()
                return render(request, 'registrar-trabajador.html', {
                    'error': 'No se pudo registrar el usuario',
                    'response': response.json(),
                    'comunas': comunas
                })
        except requests.exceptions.RequestException:
            return render(request, 'registrar-trabajador.html', {
                'error': 'Error de conexión con la API',
                'comunas': get_comunas()
            })

    comunas = get_comunas()
    return render(request, 'registrar-trabajador.html', {'comunas': comunas})



def get_comunas():
    try:
        response = requests.get('http://127.0.0.1:8000/api/comunas/')
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def login(request):
    if request.method == 'POST':
        data = {
            'correo': request.POST.get('username'),
            'contraseña': request.POST.get('password'),
        }

        try:
            response = requests.post('http://localhost:8000/api/login/', json=data)
            if response.status_code == 200:
                usuario = response.json()
                # Aquí podrías guardar en sesión si quieres
                return redirect('prueba')  # o la ruta que desees después del login
            else:
                return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
        except requests.exceptions.RequestException:
            return render(request, 'login.html', {'error': 'No se pudo conectar con el servidor'})

    return render(request, 'login.html')


def prueba(request):
    return render(request, 'prueba.html')

def vista_pagina_inicio(request):
    return render(request, 'pagina_inicio.html')

def vista_cliente_inicio(request):
    return render(request, 'cliente_inicio.html')

def vista_trabajador_inicio(request):
    return render(request, 'trabajador_inicio.html')

def vista_perfil(request):
    return render(request, 'perfil.html')

def vista_principal_pagina(request):
    return render(request, 'principal_pagina.html')

def C_trabajador(request):
    return render(request, 'c_trabajador.html')

def introduccion_trab(request):
    return render(request, 'introduccion_trab.html')