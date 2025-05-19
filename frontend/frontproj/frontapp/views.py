import requests
from django.shortcuts import render, redirect

def cpu_admin(request):
    return render(request, 'cpu_admin.html')

def acciones(request):
    return render(request, 'acciones.html')


def vista_admin_pendientes(request):
    try:
        # Trae todos (o lo que devuelva tu API) con ese querystring
        res = requests.get(
            'http://127.0.0.1:8000/api/trabajadores/?estado_verificado=false',
            timeout=5
        )
        res.raise_for_status()
        datos = res.json()
    except requests.RequestException:
        datos = []

    # Filtra sólo los que realmente tengan estado_verificado == False
    pendientes = [t for t in datos if not t.get('estado_verificado')]

    # Ajusta rutas absolutas para las imágenes
    for t in pendientes:
        for campo in ('foto_cedula', 'foto_cedula_atras', 'foto_autoretrato'):
            ruta = t.get(campo) or ''
            if ruta and not ruta.startswith('http'):
                ruta = ruta if ruta.startswith('/') else '/' + ruta
                t[campo] = 'http://127.0.0.1:8000' + ruta

    return render(request, 'pendientes_verificacion.html', {
        'trabajadores': pendientes
    })

def vista_dashboard_admin(request):
    return render(request, 'dashboard_admin.html')

from datetime import datetime

def vista_admin_boletas(request):
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    boletas = requests.get('http://127.0.0.1:8000/api/boletas/').json()

    if desde:
        desde_date = datetime.strptime(desde, "%Y-%m-%d")
        boletas = [b for b in boletas if b.get("fecha_creacion") and datetime.strptime(b["fecha_creacion"], "%Y-%m-%dT%H:%M:%S.%fZ") >= desde_date]

    if hasta:
        hasta_date = datetime.strptime(hasta, "%Y-%m-%d")
        boletas = [b for b in boletas if b.get("fecha_creacion") and datetime.strptime(b["fecha_creacion"], "%Y-%m-%dT%H:%M:%S.%fZ") <= hasta_date]

    return render(request, 'boletas_admin.html', {
        'boletas': boletas,
        'desde': desde,
        'hasta': hasta
    })


def vista_admin_usuarios(request):
    data = requests.get('http://127.0.0.1:8000/api/usuarios/').json()
    return render(request, 'usuarios_admin.html', {'usuarios': data})

def vista_admin_servicios(request):
    tipo_id = request.GET.get('tipo')
    comuna_id = request.GET.get('comuna')

    tipos = requests.get('http://127.0.0.1:8000/api/tiposervicios/').json()
    comunas = requests.get('http://127.0.0.1:8000/api/comunas/').json()
    servicios = requests.get('http://127.0.0.1:8000/api/servicios/').json()
    usuarios = requests.get('http://127.0.0.1:8000/api/usuarios/').json()

    usuarios_dict = {u['id']: u for u in usuarios}

    if tipo_id:
        servicios = [s for s in servicios if str(s.get("tipo_id")) == tipo_id]

    if comuna_id:
        servicios = [s for s in servicios if any(
            usuarios_dict.get(t_id, {}).get("comuna") == int(comuna_id)
            for t_id in s.get("trabajadores", [])
        )]

    return render(request, 'servicios_admin.html', {
        'servicios': servicios,
        'tipos': tipos,
        'comunas': comunas,
        'tipo_seleccionado': tipo_id,
        'comuna_seleccionada': comuna_id
    })



def vista_admin_trabajadores(request):
    especialidad_id = request.GET.get('especialidad')
    comuna_id = request.GET.get('comuna')

    especialidades = requests.get('http://127.0.0.1:8000/api/especialidades/').json()
    comunas = requests.get('http://127.0.0.1:8000/api/comunas/').json()

    trabajadores = requests.get('http://127.0.0.1:8000/api/trabajadores/').json()

    # Filtrar por especialidad y comuna
    if especialidad_id:
        trabajadores = [t for t in trabajadores if str(t['especialidad']['id']) == especialidad_id]

    if comuna_id:
        trabajadores = [t for t in trabajadores if str(t['usuario']['comuna']) == comuna_id]

    return render(request, 'trabajadores_admin.html', {
        'trabajadores': trabajadores,
        'especialidades': especialidades,
        'comunas': comunas,
        'especialidad_seleccionada': especialidad_id,
        'comuna_seleccionada': comuna_id
    })

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

def vista_perfil_trabajador(request,):
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
def vista_perfil_trabajador_id(request, usuario_id):
    trabajador_data = {}

    try:
        trab_response = requests.get(f'http://localhost:8000/api/trabajadores/?usuario={usuario_id}')
        if trab_response.status_code == 200:
            trabajadores = trab_response.json()
            if trabajadores:
                trabajador_data = trabajadores[0]
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