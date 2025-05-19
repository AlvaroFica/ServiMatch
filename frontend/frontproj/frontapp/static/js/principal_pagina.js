// static/js/principal_pagina.js

document.addEventListener("DOMContentLoaded", () => {
  // 1. Inicializar mapa
  const mapa = L.map('mapa').setView([-33.4489, -70.6693], 13);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; CartoDB'
  }).addTo(mapa);

  let markersLayer = L.layerGroup().addTo(mapa);

  // 2. Geolocalización automática
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      pos => {
        const { latitude: lat, longitude: lon } = pos.coords;
        mapa.setView([lat, lon], 16);
        L.marker([lat, lon])
          .addTo(mapa)
          .bindPopup("¡Estás aquí!")
          .openPopup();
      },
      err => console.error("Error geolocalización:", err.message),
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
  }

  // 3. Botón para centrar manualmente
  document.getElementById("centrar-ubicacion").addEventListener("click", () => {
    if (!navigator.geolocation) return alert("Tu navegador no soporta geolocalización.");
    navigator.geolocation.getCurrentPosition(
      pos => {
        const { latitude: lat, longitude: lon } = pos.coords;
        mapa.setView([lat, lon], 16);
        L.marker([lat, lon])
          .addTo(mapa)
          .bindPopup("¡Tu ubicación actual!")
          .openPopup();
      },
      () => alert("No se pudo obtener tu ubicación."),
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
  });

  // 4. Mostrar marcadores con popup “Ver Perfil” + “Contratar”
  async function mostrarTrabajadores(trabajadores) {
    markersLayer.clearLayers();

    trabajadores.forEach(trab => {
      if (!trab.latitud || !trab.longitud) return;

      // Icono según especialidad
      const icono = trab.especialidad
        ? obtenerIconoPorEspecialidad(trab.especialidad.nombre_esp)
        : undefined;

      // Extraer ID de servicio: si 'trab.servicios' es array de objetos, usar .id
      let servicioId = null;
      if (Array.isArray(trab.servicios) && trab.servicios.length) {
        const s = trab.servicios[0];
        servicioId = (typeof s === 'object' && s !== null) ? s.id : s;
      }

      // Construir el HTML del popup
      const popupContent = `
        <div style="text-align:center; font-family:Arial,sans-serif;">
          <strong>${trab.usuario.nombre} ${trab.usuario.apellido}</strong><br/>
          <em>${trab.especialidad?.nombre_esp || 'Sin especialidad'}</em><br/><br/>
          <a
            href="/perfil_trabajador/${trab.usuario.id}/"
            style="
              display:inline-block;
              margin:0 4px 4px 0;
              padding:6px 12px;
              background:#3498db;
              color:#fff;
              border-radius:4px;
              text-decoration:none;
              font-weight:600;
            "
          >👤 Ver Perfil</a>
          ${servicioId
            ? `<a
                 href="/planes_servicio/${servicioId}/"
                 style="
                   display:inline-block;
                   margin:0 0 4px 4px;
                   padding:6px 12px;
                   background:#27ae60;
                   color:#fff;
                   border-radius:4px;
                   text-decoration:none;
                   font-weight:600;
                 "
               >🛠️ Contratar</a>`
            : ''}
        </div>
      `;

      L.marker([trab.latitud, trab.longitud], icono ? { icon: icono } : undefined)
        .bindPopup(popupContent)
        .addTo(markersLayer);
    });

    // Centrar en el primer trabajador
    const primero = trabajadores.find(t => t.latitud && t.longitud);
    if (primero) mapa.setView([primero.latitud, primero.longitud], 14);
  }

  // 5. Cargar todos los trabajadores al iniciar
  async function cargarTodosTrabajadores() {
    try {
      const res = await fetch("http://localhost:8000/api/trabajadores/");
      const lista = await res.json();
      mostrarTrabajadores(lista);
    } catch (e) {
      console.error("Error cargando trabajadores:", e);
    }
  }
  cargarTodosTrabajadores();

  // 6. Buscador principal
  document.getElementById("btn-buscar").addEventListener("click", buscarServicio);
  async function buscarServicio() {
    const texto = document.getElementById("busqueda-servicio").value.trim().toLowerCase();
    if (!texto) return;
    try {
      const res = await fetch("http://localhost:8000/api/trabajadores/");
      const trabajadores = await res.json();
      const filtrados = trabajadores.filter(trab =>
        trab.latitud &&
        trab.longitud &&
        trab.especialidad &&
        trab.especialidad.nombre_esp.toLowerCase().includes(texto)
      );
      if (filtrados.length === 0) {
        return alert("No se encontraron trabajadores con esa especialidad y ubicación.");
      }
      mostrarTrabajadores(filtrados);
    } catch (e) {
      console.error("Error buscando trabajadores:", e);
      alert("Hubo un error al buscar servicios.");
    }
  }

  // 7. Sugerencias al tipear
  const listaSug = document.getElementById("sugerencias");
  document.getElementById("busqueda-servicio").addEventListener("input", () => {
    const txt = document.getElementById("busqueda-servicio").value.toLowerCase().trim();
    listaSug.innerHTML = "";
    if (!txt) return;

    const ejemplos = [
      "Gasfiter","Electricista","Carpintero","Pintor","Cerrajero",
      "Jardinero","Albañil","Refrigeración","Aire acondicionado",
      "Mecánico automotriz","Mecánico de bicicletas","Yesero",
      "Soldador","Techador","Pisos","Tapicero","Paisajista"
    ];

    ejemplos
      .filter(s => s.toLowerCase().includes(txt))
      .forEach(s => {
        const li = document.createElement("li");
        li.textContent = s;
        li.onclick = () => {
          document.getElementById("busqueda-servicio").value = s;
          listaSug.innerHTML = "";
        };
        listaSug.appendChild(li);
      });
  });

  // 8. Menú superior dinámico
  (async () => {
    const barra = document.getElementById("barra-superior");
    const usuarioId = localStorage.getItem("usuario_id");
    if (!usuarioId) {
      barra.innerHTML = `<a href="/login/" class="btn-inactivo">INICIAR SESIÓN</a>`;
      return;
    }
    let html = `<a href="/logout/" class="opcion-menu"><i class="fa fa-sign-out-alt"></i> Cerrar sesión</a>`;
    try {
      const resp = await fetch(`http://localhost:8000/api/trabajadores/?usuario=${usuarioId}`);
      const arr = await resp.json();
      if (arr.length > 0) {
        html += `
          <a href="/perfil_trabajador/${usuarioId}/" class="btn-inactivo">PANEL TRABAJADOR</a>
          <a href="/perfil_trabajador/${usuarioId}/" class="btn-inactivo">PERFIL</a>
        `;
      } else {
        html += `
          <a href="/pagina_inicio/" class="btn-inactivo">SOLO CLIENTE</a>
          <a href="/c_trabajador/" class="btn-inactivo">SER TRABAJADOR</a>
        `;
      }
    } catch {
      console.error("Error verificando rol");
    }
    barra.innerHTML = html;
  })();
});

// 9. Iconos por especialidad
function obtenerIconoPorEspecialidad(nombreEspecialidad) {
  const iconos = {
    "Gasfiter":"gasfiter.png","Electricista":"electricista.png","Carpintero":"carpintero.png",
    "Pintor":"pintor.png","Cerrajero":"cerrajero.png","Jardinero":"jardinero.png",
    "Albañil":"albañil.png","Técnico en refrigeración":"refrigeracion.png",
    "Técnico en aire acondicionado":"aire_acondicionado.png",
    "Mecánico automotriz":"mecanico_auto.png","Mecánico de bicicletas":"mecanico_bici.png",
    "Yesero":"yesero.png","Soldador":"soldador.png","Techador":"techador.png",
    "Instalador de pisos":"pisos.png","Tapicero":"tapicero.png",
    "Paisajista":"paisajista.png","Podador de árboles":"podador.png",
    "Flete y mudanza":"flete.png","Técnico en computación":"computacion.png"
  };
  const iconoURL = iconos[nombreEspecialidad] || "default.png";
  return L.icon({
    iconUrl: `/static/icons/${iconoURL}`,
    iconSize: [30, 40],
    iconAnchor: [15, 40],
    popupAnchor: [0, -35]
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const userId = Number(localStorage.getItem('usuario_id'));
  if (!userId) return;

  // Mostrar bolita si hay chats
  fetch(`http://localhost:8000/api/chats/usuario/${userId}/`)
    .then(r => r.json())
    .then(arr => {
      if (arr.length > 0) {
        const bolita = document.getElementById('noti-chat');
        if (bolita) bolita.style.display = 'block';
      }
    });

  // Redirección al chat (primer chat del usuario)
  const btnChat = document.getElementById('btn-chat');
  if (btnChat) {
    btnChat.addEventListener('click', function(e) {
      e.preventDefault();
      fetch(`http://localhost:8000/api/chats/usuario/${userId}/`)
        .then(r => r.json())
        .then(arr => {
          if (arr.length > 0) {
            window.location.href = `/chat/${arr[0].id}/`;
          } else {
            alert("No tienes chats activos.");
          }
        });
    });
  }
});
