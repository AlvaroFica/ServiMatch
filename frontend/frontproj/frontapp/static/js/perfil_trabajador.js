// static/js/perfil_trabajador.js

document.addEventListener('DOMContentLoaded', async () => {
  // 1) ID de usuario: URL o sesión
  const pathMatch = window.location.pathname.match(/\/perfil_trabajador\/(\d+)\/?$/);
  const usuarioParam = pathMatch
    ? pathMatch[1]
    : localStorage.getItem('usuario_id');
  if (!usuarioParam) {
    alert('Sesión expirada. Inicia sesión de nuevo.');
    return window.location.href = '/login/';
  }

  try {
    // 2) Datos del trabajador
    const res = await fetch(`http://localhost:8000/api/trabajadores/?usuario=${usuarioParam}`);
    if (!res.ok) throw new Error(`Status ${res.status}`);
    const arr = await res.json();
    if (!arr.length) {
      alert('Trabajador no encontrado.');
      return;
    }
    const t = arr[0];

    // 3) Avatar
    const avatarDiv = document.getElementById('avatar');
    if (t.usuario.foto_perfil) {
      const img = document.createElement('img');
      let src = t.usuario.foto_perfil;
      if (!src.startsWith('http')) {
        src = `http://localhost:8000${src.startsWith('/') ? '' : '/'}${src}`;
      }
      img.src = src;
      img.alt = `${t.usuario.nombre} avatar`;
      avatarDiv.appendChild(img);
    } else {
      avatarDiv.innerHTML = '<i class="fa fa-user fa-3x"></i>';
    }

    // 4) Nombre y especialidad
    document.getElementById('nombre-trabajador').innerText =
      `${t.usuario.nombre} ${t.usuario.apellido}`;
    document.getElementById('especialidad-trabajador').innerText =
      t.especialidad?.nombre_esp || 'Sin especialidad';

    // 5) Antigüedad
    const fecha = new Date(t.usuario.fecha_creacion);
    document.getElementById('fecha-creacion').innerText =
      fecha.toLocaleDateString('es-CL', { year:'numeric', month:'long' });

    // 6) Cantidad de servicios
    document.getElementById('cantidad-servicios').innerText =
      t.servicios?.length ?? 0;

    // 7) Botón Contratar
    const btnContratar = document.getElementById('btn-contratar');
    if (btnContratar) {
      const servicioId = Array.isArray(t.servicios) && t.servicios.length
        ? (typeof t.servicios[0] === 'object' ? t.servicios[0].id : t.servicios[0])
        : null;
      if (servicioId) {
        btnContratar.href = `/planes_servicio/${servicioId}/`;
      } else {
        btnContratar.style.display = 'none';
      }
    }

    // 8) Portafolio
    const portfolioGrid = document.querySelector('.portfolio-grid');
    portfolioGrid.innerHTML = '';
    const pics = [t.foto_cedula, t.foto_cedula_atras, t.foto_autoretrato].filter(Boolean);
    pics.forEach(url => {
      const thumb = document.createElement('div');
      thumb.className = 'thumb';
      const im = document.createElement('img');
      let s = url.startsWith('http')
        ? url
        : `http://localhost:8000${url.startsWith('/') ? '' : '/'}${url}`;
      im.src = s;
      thumb.appendChild(im);
      portfolioGrid.appendChild(thumb);
    });

    // 9) Evaluaciones (ejemplo estático)
    const reviewsGrid = document.querySelector('.review-tags');
    reviewsGrid.innerHTML = '';
    ['Atención a los detalles','Rapidez','Puntualidad']
      .forEach(text => {
        const span = document.createElement('span');
        span.className = 'tag';
        span.innerText = text;
        reviewsGrid.appendChild(span);
      });

    // 10) Mostrar/ocultar menú-servicios
    const linkMis  = document.getElementById('link-mis-servicios');
    const linkEdit = document.getElementById('link-editar-info');
    const menuServ = document.getElementById('menu-servicios');
    const loggedId = localStorage.getItem('usuario_id');
    const isOwner = String(usuarioParam) === String(loggedId);

    if (linkMis && linkEdit && menuServ) {
      if (isOwner) {
        if (!t.estado_verificado) {
          linkMis.style.display  = 'none';
          linkEdit.style.display = 'none';
          const aviso = document.createElement('p');
          aviso.className = 'aviso-pendiente';
          aviso.innerText =
            'Tu cuenta está en revisión. No puedes crear ni ver servicios hasta ser verificado.';
          menuServ.insertBefore(aviso, linkMis);
        }
      } else {
        linkMis.style.display  = 'none';
        linkEdit.style.display = 'none';
      }
    }

  } catch (err) {
    console.error('Error cargando perfil:', err);
    alert('No se pudo cargar la información del perfil.');
  }
});
