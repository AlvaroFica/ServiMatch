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
                usuario = response.json()

                # Crear trabajador asociado inmediatamente
                trabajador_data = {
                    "usuario": usuario['id'],
                    "especialidad": None,  # o un ID válido si tienes una por defecto
                    "estado_verificado": False
                }

                # Puedes enviar campos vacíos de imagen si aún no los tienes
                requests.post("http://127.0.0.1:8000/api/trabajadores/", data=trabajador_data)

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
                request.session['usuario_id'] = usuario['usuario_id']
                request.session['nombre'] = usuario['nombre']
                print(">>> Login exitoso, ID guardado en sesión:", request.session['usuario_id'])
                return redirect('principal_pagina')
            else:
                return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
        except requests.exceptions.RequestException:
            return render(request, 'login.html', {'error': 'No se pudo conectar con el servidor'})

    return render(request, 'login.html')

    
def logout(request):
    request.session.flush()  # Esto borra TODA la sesión
    return redirect('login')



def prueba(request):
    return render(request, 'prueba.html')

def vista_pagina_inicio(request):
    return render(request, 'pagina_inicio.html')

def vista_cliente_inicio(request):
    return render(request, 'cliente_inicio.html')

def vista_perfil_trabajador(request):
    usuario_id = request.session.get('usuario_id')
    trabajador_data = {}
    
    if usuario_id:
        try:
            trab_response = requests.get(f'http://localhost:8000/api/trabajadores/?usuario={usuario_id}')
            if trab_response.status_code == 200:
                trabajadores = trab_response.json()
                if trabajadores:
                    trabajador_data = trabajadores[0]  # solo uno porque es OneToOne
        except requests.exceptions.RequestException:
            pass

    return render(request, 'perfil_trabajador.html', {
        'trabajador': trabajador_data
    })

def vista_mis_servicios(request):
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return render(request, 'mis_servicios.html', {'servicios': []})

    # Paso 1: obtener el trabajador del usuario
    try:
        r_trab = requests.get(f'http://localhost:8000/api/trabajadores/?usuario={usuario_id}')
        trabajador_data = r_trab.json()
        if not trabajador_data:
            return render(request, 'mis_servicios.html', {'servicios': []})
        trabajador_id = trabajador_data[0]['id']
    except:
        return render(request, 'mis_servicios.html', {'servicios': []})

    # Paso 2: obtener todos los servicios
    try:
        r_serv = requests.get('http://localhost:8000/api/servicios/')
        servicios_data = r_serv.json()
    except:
        servicios_data = []

    # Paso 3: filtrar solo los servicios de este trabajador
    servicios_usuario = []
    for serv in servicios_data:
        if trabajador_id in serv.get('trabajadores', []):
            # Añadir lista de imágenes vacía si no hay campo
            if 'imagenes' not in serv:
                serv['imagenes'] = []
            servicios_usuario.append(serv)

    return render(request, 'mis_servicios.html', {'servicios': servicios_usuario})


def vista_agregar_servicio(request):
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')

        # Obtener el trabajador asociado
        trabajador_resp = requests.get(f'http://localhost:8000/api/trabajadores/?usuario={usuario_id}')
        trabajadores = trabajador_resp.json()
        if trabajadores:
            trabajador_id = trabajadores[0]['id']

            # Crear el servicio
            data = {
                "nombre_serv": request.POST.get("nombre_serv"),
                "tipo": int(request.POST.get("tipo")),
                "trabajadores": [trabajador_id],
            }

            servicio_resp = requests.post('http://localhost:8000/api/servicios/', json=data)

            if servicio_resp.status_code == 201:
                servicio_id = servicio_resp.json()['id']

                # Subir imágenes si se mandaron
                imagenes = request.FILES.getlist('imagenes')
                if imagenes:
                    files = [('imagenes', img) for img in imagenes]
                    upload_resp = requests.post(
                        f'http://localhost:8000/api/servicios/{servicio_id}/imagenes/',
                        files=files
                    )

                    if upload_resp.status_code not in [200, 201]:
                        print(">>> Error subiendo imágenes:", upload_resp.status_code, upload_resp.text)

                return redirect('mis_servicios')

        return render(request, 'agregar_servicio.html', {'error': 'No se pudo crear el servicio.'})

    # GET → cargar tipos
    try:
        tipos = requests.get('http://localhost:8000/api/tiposervicios/').json()
    except:
        tipos = []

    return render(request, 'agregar_servicio.html', {'tipos_servicio': tipos})



def vista_perfil(request):
    return render(request, 'perfil.html')

def vista_principal_pagina(request):
    usuario_id = request.session.get('usuario_id')
    print(">>> vista_principal_pagina: usuario_id en sesión:", usuario_id)

    es_trabajador = False
    nombre_usuario = None

    if usuario_id:
        try:
            # Obtener usuario desde API
            response = requests.get(f'http://127.0.0.1:8000/api/usuarios/{usuario_id}/')
            if response.status_code == 200:
                usuario_data = response.json()
                nombre_usuario = usuario_data['nombre']

                # Verificar si es trabajador
                trab_response = requests.get(f'http://127.0.0.1:8000/api/trabajadores/?usuario={usuario_id}')
                if trab_response.status_code == 200:
                    trabajadores = trab_response.json()
                    es_trabajador = len(trabajadores) > 0
        except:
            print(">>> Error consultando API")

    return render(request, 'principal_pagina.html', {
        'logueado': bool(usuario_id),
        'es_trabajador': es_trabajador,
        'nombre_usuario': nombre_usuario
    })

def C_trabajador(request):
    return render(request, 'c_trabajador.html')

def introduccion_trab(request):
    return render(request, 'introduccion_trab.html')

def vista_registro_trabajador(request):
    return render(request, 'registro_trabajador.html')  # crea esta plantilla si quieres

def vista_planes_servicio(request, servicio_id):
    return render(request, 'planes_servicios.html', {'servicio_id': servicio_id})

def vista_mensaje_exito(request):
    return render(request, 'mensaje_exito.html')

def vista_ver_planes(request, servicio_id):
    return render(request, 'ver_planes.html', {'servicio_id': servicio_id})

API_BASE = 'http://127.0.0.1:8000/api'

def historial_servicio(request):
    try:
        resp = requests.get(f'{API_BASE}/servicios/')
        servicios = resp.json() if resp.status_code == 200 else []
    except requests.RequestException:
        servicios = []
    return render(request, 'historial-servicio.html', {'servicios': servicios})

def historial_detalle(request, servicio_id):
    try:
        resp_serv = requests.get(f'{API_BASE}/servicios/{servicio_id}/')
        servicio = resp_serv.json() if resp_serv.status_code == 200 else {}
    except requests.RequestException:
        servicio = {}

    try:
        resp_cal = requests.get(f'{API_BASE}/servicios/{servicio_id}/calificaciones/')
        calificaciones = resp_cal.json() if resp_cal.status_code == 200 else []
    except requests.RequestException:
        calificaciones = []

    return render(request, 'historial-detalle.html', {
        'servicio': servicio,
        'calificaciones': calificaciones
    })
