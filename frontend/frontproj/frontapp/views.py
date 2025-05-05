import requests
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        data = {
            'nombre': request.POST.get('nombre'),
            'apellido': request.POST.get('apellido'),
            'correo': request.POST.get('correo'),
            'telefono': request.POST.get('celular'),
            'fecha_nac': request.POST.get('fecha_nacimiento'),
            'comuna': request.POST.get('comuna'),  # Debe ser el ID
            'contraseña': request.POST.get('contraseña'),
        }

        try:
            response = requests.post('http://127.0.0.1:8000/api/usuarios/', data=data)
            if response.status_code == 201:
                return redirect('login')
            else:
                comunas = get_comunas()
                return render(request, 'registrar-trabajador.html', {
                    'error': 'No se pudo registrar el usuario',
                    'response': response.json(),
                    'comunas': comunas
                })
        except requests.exceptions.RequestException as e:
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
    return render(request, 'login.html')
