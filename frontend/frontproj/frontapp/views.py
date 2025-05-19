import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Servicio, CalificacionEtiqueta, Etiqueta
from .forms import EtiquetasForm

API_BASE = 'http://127.0.0.1:8000/api'

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
            response = requests.post(f'{API_BASE}/usuarios/', data=data, files=files)
            if response.status_code == 201:
                usuario = response.json()
                trabajador_data = {
                    "usuario": usuario['id'],
                    "especialidad": None,
                    "estado_verificado": False
                }
                requests.post(f'{API_BASE}/trabajadores/', data=trabajador_data)
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
        resp = requests.get(f'{API_BASE}/comunas/')
        return resp.json() if resp.status_code == 200 else []
    except requests.exceptions.RequestException:
        return []

def login(request):
    if request.method == 'POST':
        data = {
            'correo': request.POST.get('username'),
            'contraseña': request.POST.get('password'),
        }
        try:
            resp = requests.post(f'{API_BASE}/login/', json=data)
            if resp.status_code == 200:
                u = resp.json()
                request.session['usuario_id'] = u['usuario_id']
                request.session['nombre'] = u['nombre']
                return redirect('principal_pagina')
            else:
                return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
        except requests.exceptions.RequestException:
            return render(request, 'login.html', {'error': 'No se pudo conectar con el servidor'})
    return render(request, 'login.html')

def logout(request):
    request.session.flush()
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
            resp = requests.get(f'{API_BASE}/trabajadores/?usuario={usuario_id}')
            if resp.status_code == 200 and resp.json():
                trabajador_data = resp.json()[0]
        except requests.exceptions.RequestException:
            pass
    return render(request, 'perfil_trabajador.html', {'trabajador': trabajador_data})

def vista_mis_servicios(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return render(request, 'mis_servicios.html', {'servicios': []})
    try:
        r = requests.get(f'{API_BASE}/trabajadores/?usuario={usuario_id}')
        trab = r.json()
        if not trab:
            return render(request, 'mis_servicios.html', {'servicios': []})
        trabajador_id = trab[0]['id']
    except requests.exceptions.RequestException:
        return render(request, 'mis_servicios.html', {'servicios': []})

    try:
        r = requests.get(f'{API_BASE}/servicios/')
        servicios = r.json()
    except requests.exceptions.RequestException:
        servicios = []

    servicios_usuario = []
    for s in servicios:
        if trabajador_id in s.get('trabajadores', []):
            s.setdefault('imagenes', [])
            servicios_usuario.append(s)
    return render(request, 'mis_servicios.html', {'servicios': servicios_usuario})

def vista_agregar_servicio(request):
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')
        try:
            r = requests.get(f'{API_BASE}/trabajadores/?usuario={usuario_id}')
            trabajador_id = r.json()[0]['id']
        except:
            trabajador_id = None

        if trabajador_id:
            data = {
                "nombre_serv": request.POST.get("nombre_serv"),
                "tipo": int(request.POST.get("tipo")),
                "trabajadores": [trabajador_id],
            }
            resp = requests.post(f'{API_BASE}/servicios/', json=data)
            if resp.status_code == 201:
                sid = resp.json()['id']
                imgs = request.FILES.getlist('imagenes')
                if imgs:
                    files = [('imagenes', img) for img in imgs]
                    requests.post(f'{API_BASE}/servicios/{sid}/imagenes/', files=files)
                return redirect('mis_servicios')
        return render(request, 'agregar_servicio.html', {'error': 'No se pudo crear el servicio.'})

    try:
        tipos = requests.get(f'{API_BASE}/tiposervicios/').json()
    except requests.exceptions.RequestException:
        tipos = []
    return render(request, 'agregar_servicio.html', {'tipos_servicio': tipos})

def vista_perfil(request):
    return render(request, 'perfil.html')

def vista_principal_pagina(request):
    usuario_id = request.session.get('usuario_id')
    es_trab = False
    nombre = None
    if usuario_id:
        try:
            r = requests.get(f'{API_BASE}/usuarios/{usuario_id}/')
            if r.status_code == 200:
                nombre = r.json()['nombre']
                rt = requests.get(f'{API_BASE}/trabajadores/?usuario={usuario_id}')
                es_trab = bool(rt.json())
        except requests.exceptions.RequestException:
            pass
    # Obtener servicios y etiquetas para mostrar en la página principal
    try:
        servicios = requests.get(f'{API_BASE}/servicios/').json()
    except requests.exceptions.RequestException:
        servicios = []
    try:
        etiquetas = requests.get(f'{API_BASE}/etiquetas/').json()
    except requests.exceptions.RequestException:
        etiquetas = []

    return render(request, 'principal_pagina.html', {
        'logueado': bool(usuario_id),
        'es_trabajador': es_trab,
        'nombre_usuario': nombre,
        'servicios': servicios,
        'etiquetas': etiquetas,
    })

def C_trabajador(request):
    return render(request, 'c_trabajador.html')

def introduccion_trab(request):
    return render(request, 'introduccion_trab.html')

def vista_registro_trabajador(request):
    return render(request, 'registro_trabajador.html')

def vista_planes_servicio(request, servicio_id):
    return render(request, 'planes_servicios.html', {'servicio_id': servicio_id})

def vista_mensaje_exito(request):
    return render(request, 'mensaje_exito.html')

def vista_ver_planes(request, servicio_id):
    return render(request, 'ver_planes.html', {'servicio_id': servicio_id})

def historial_servicio(request):
    try:
        resp = requests.get(f'{API_BASE}/servicios/')
        servicios = resp.json() if resp.status_code == 200 else []
    except requests.exceptions.RequestException:
        servicios = []

    for s in servicios:
        try:
            etiquetas_resp = requests.get(f'{API_BASE}/servicios/{s["id"]}/etiquetas/')
            s['etiquetas'] = etiquetas_resp.json() if etiquetas_resp.status_code == 200 else []
        except requests.exceptions.RequestException:
            s['etiquetas'] = []
    return render(request, 'historial-servicio.html', {'servicios': servicios})

def historial_detalle(request, servicio_id):
    # 1. Traer servicio
    try:
        resp = requests.get(f'{API_BASE}/servicios/{servicio_id}/')
        servicio = resp.json() if resp.status_code == 200 else {}
    except requests.exceptions.RequestException:
        return render(request, "404.html", status=404)

    # 2. Calificaciones (opcional; no afecta al problema)
    try:
        r2 = requests.get(f'{API_BASE}/servicios/{servicio_id}/calificaciones/')
        calificaciones = r2.json() if r2.status_code == 200 else []
    except requests.exceptions.RequestException:
        calificaciones = []

    # 3. Comprobamos sesión
    logueado = bool(request.session.get("usuario_id"))

    return render(
        request,
        "historial-detalle.html",
        {
            "servicio": servicio,
            "calificaciones": calificaciones,
            "logueado": logueado,   # ← **importante**
        },
    )

def calificar_servicio(request, servicio_id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debes iniciar sesión para calificar.")
        return redirect('login')

    # Obtener servicio desde la API
    resp = requests.get(f'{API_BASE}/servicios/{servicio_id}/')
    if resp.status_code != 200:
        return render(request, '404.html', status=404)

    servicio = resp.json()

    if request.method == 'POST':
        valor = request.POST.get('valor')
        comentario = request.POST.get('comentario')

        request.session['calificacion'] = {
            'servicio_id': servicio_id,
            'usuario_id': usuario_id,
            'valor': valor,
            'comentario': comentario
        }

        return redirect('calificar-etiquetas', servicio_id=servicio_id)

    return render(request, 'calificar-servicio.html', {
        'trabajador': servicio['trabajadores'][0] if servicio['trabajadores'] else {},
        'servicio_id': servicio_id
    })

def ver_etiquetas(request, servicio_id):
    from django.db.models import Count, Q
    servicio = get_object_or_404(Servicio, id=servicio_id)
    etiquetas = Etiqueta.objects.annotate(
        menciones=Count(
            'calificacionetiqueta__etiquetas',
            filter=Q(calificacionetiqueta__servicio=servicio)
        )
    ).order_by('-menciones')
    return render(request, 'ver-etiquetas.html', {
        'servicio': servicio,
        'etiquetas': etiquetas
    })

def calificar_etiquetas(request, servicio_id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    etiquetas = [
        "Puntual", "Amable", "Rápido", "Atento",
        "Profesional", "Detallista", "Respetuoso", "Limpio", "Empático"
    ]

    if request.method == 'POST':
        seleccionadas = request.POST.get('etiquetas', "").split(",")

        datos_previos = request.session.get('calificacion')
        if not datos_previos:
            messages.error(request, "No se encontró la información previa.")
            return redirect('calificar-servicio', servicio_id=servicio_id)

        data = {
            'servicio': servicio_id,
            'usuario': usuario_id,
            'valor': datos_previos['valor'],
            'comentario': datos_previos['comentario'],
            'etiquetas': seleccionadas
        }

        r = requests.post(f'{API_BASE}/calificaciones/', json=data)
        if r.status_code in (200, 201):
            messages.success(request, "¡Gracias por tu calificación!")
            request.session.pop('calificacion', None)
            return redirect('historial-detalle', servicio_id=servicio_id)
        else:
            messages.error(request, "Error al guardar la calificación.")

    return render(request, 'calificar-etiquetas.html', {
        'etiquetas': etiquetas,
        'servicio_id': servicio_id
    })
