document.addEventListener("DOMContentLoaded", () => {
    const mapa = L.map('mapa').setView([-33.4489, -70.6693], 13);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; CartoDB'
    }).addTo(mapa);

    let markersLayer = L.layerGroup().addTo(mapa);

    // Geolocalización automática al cargar
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                mapa.setView([lat, lon], 16);

                L.marker([lat, lon])
                    .addTo(mapa)
                    .bindPopup("¡Estás aquí!")
                    .openPopup();
            },
            error => {
                console.error("No se pudo obtener la ubicación:", error.message);
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    } else {
        alert("Tu navegador no soporta geolocalización.");
    }

    // Botón manual para centrar ubicación
    document.getElementById("centrar-ubicacion").addEventListener("click", () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                position => {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;

                    mapa.setView([lat, lon], 16);

                    L.marker([lat, lon])
                        .addTo(mapa)
                        .bindPopup("¡Tu ubicación actual!")
                        .openPopup();
                },
                error => {
                    alert("No se pudo obtener tu ubicación.");
                    console.error(error);
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                }
            );
        } else {
            alert("Tu navegador no soporta geolocalización.");
        }
    });

    async function mostrarTrabajadores(trabajadores) {
        markersLayer.clearLayers();
        let encontrados = 0;

        trabajadores.forEach(trab => {
            if (trab.latitud && trab.longitud) {
                const icono = trab.especialidad ? obtenerIconoPorEspecialidad(trab.especialidad.nombre_esp) : null;
                const popupContent = `
                    <strong>${trab.usuario.nombre} ${trab.usuario.apellido}</strong><br>
                    Especialidad: ${trab.especialidad ? trab.especialidad.nombre_esp : 'No definida'}<br>
                    <a href="/perfil_trabajador/${trab.usuario.id}/" class="btn btn-sm btn-primary mt-2">Ver Perfil</a>
                `;

                const marker = L.marker([trab.latitud, trab.longitud], icono ? { icon: icono } : undefined)
                    .bindPopup(popupContent);

                markersLayer.addLayer(marker);
                encontrados++;
            }
        });

        if (encontrados > 0) {
            const primero = trabajadores.find(t => t.latitud && t.longitud);
            if (primero) mapa.setView([primero.latitud, primero.longitud], 14);
        }
    }

    async function cargarTodosTrabajadores() {
        try {
            const response = await fetch("http://localhost:8000/api/trabajadores/");
            const trabajadores = await response.json();
            mostrarTrabajadores(trabajadores);
        } catch (error) {
            console.error("Error cargando trabajadores:", error);
        }
    }

    cargarTodosTrabajadores();

    // Buscador principal
    document.getElementById("btn-buscar").addEventListener("click", buscarServicio);

    async function buscarServicio() {
        const texto = document.getElementById("busqueda-servicio").value.trim().toLowerCase();
        if (!texto) return;

        try {
            const response = await fetch("http://localhost:8000/api/trabajadores/");
            const trabajadores = await response.json();

            const filtrados = trabajadores.filter(trab =>
                trab.latitud &&
                trab.longitud &&
                trab.especialidad &&
                trab.especialidad.nombre_esp.toLowerCase().includes(texto)
            );

            if (filtrados.length === 0) {
                alert("No se encontraron trabajadores ofreciendo ese servicio con ubicación.");
            }

            mostrarTrabajadores(filtrados);

        } catch (e) {
            console.error("Error buscando trabajadores:", e);
            alert("Hubo un error al buscar servicios.");
        }
    }

    // Sugerencias
    document.getElementById("busqueda-servicio").addEventListener("input", mostrarSugerencias);
    const lista = document.getElementById("sugerencias");

    function mostrarSugerencias() {
        const texto = document.getElementById("busqueda-servicio").value.toLowerCase().trim();
        lista.innerHTML = "";
        if (texto === "") return;

        const ejemplos = [
            "Gasfiter", "Electricista", "Carpintero", "Pintor", "Cerrajero", "Jardinero", "Albañil",
            "Técnico en refrigeración", "Técnico en aire acondicionado", "Mecánico automotriz",
            "Mecánico de bicicletas", "Yesero", "Soldador", "Techador", "Instalador de pisos",
            "Tapicero", "Paisajista", "Podador de árboles", "Flete y mudanza", "Técnico en computación"
        ];

        const filtrados = ejemplos.filter(servicio =>
            servicio.toLowerCase().includes(texto)
        );

        filtrados.forEach(servicio => {
            const item = document.createElement("li");
            item.textContent = servicio;
            item.onclick = () => {
                document.getElementById("busqueda-servicio").value = servicio;
                lista.innerHTML = "";
            };
            lista.appendChild(item);
        });
    }

    // Barra superior según sesión
    const usuarioId = localStorage.getItem("usuario_id");
    const barra = document.getElementById("barra-superior");

    if (!usuarioId) {
        barra.innerHTML = `<a href="/login/" class="btn-inactivo">INICIAR SESIÓN</a>`;
    } else {
        (async () => {
            let contenido = `<a href="/logout/" class="opcion-menu"><i class="fa fa-sign-out-alt"></i> Cerrar sesión</a>`;
            try {
                const response = await fetch(`http://localhost:8000/api/trabajadores/?usuario=${usuarioId}`);
                const trabajadores = await response.json();

                if (trabajadores.length > 0) {
                    contenido += `<a href="/perfil_trabajador/" class="btn-inactivo">PANEL TRABAJADOR</a>
                                  <a href="/perfil_trabajador/" class="btn-inactivo">PERFIL</a>`;
                } else {
                    contenido += `<a href="/pagina_inicio/" class="btn-inactivo">SOLO CLIENTE</a>
                                  <a href="/c_trabajador/" class="btn-inactivo">SER TRABAJADOR</a>`;
                }
            } catch (err) {
                console.error("Error al verificar rol de usuario:", err);
                contenido += `<p>Error cargando opciones</p>`;
            }
            barra.innerHTML = contenido;
        })();
    }
});

// Íconos por especialidad
function obtenerIconoPorEspecialidad(nombreEspecialidad) {
    const iconos = {
        "Gasfiter": "gasfiter.png",
        "Electricista": "electricista.png",
        "Carpintero": "carpintero.png",
        "Pintor": "pintor.png",
        "Cerrajero": "cerrajero.png",
        "Jardinero": "jardinero.png",
        "Albañil": "albañil.png",
        "Técnico en refrigeración": "refrigeracion.png",
        "Técnico en aire acondicionado": "aire_acondicionado.png",
        "Mecánico automotriz": "mecanico_auto.png",
        "Mecánico de bicicletas": "mecanico_bici.png",
        "Técnico en electrodomésticos": "electrodomesticos.png",
        "Yesero": "yesero.png",
        "Soldador": "soldador.png",
        "Techador": "techador.png",
        "Instalador de pisos": "pisos.png",
        "Tapicero": "tapicero.png",
        "Paisajista": "paisajista.png",
        "Podador de árboles": "podador.png",
        "Flete y mudanza": "flete.png",
        "Técnico en computación": "computacion.png"
    };

    const iconoURL = iconos[nombreEspecialidad] || "default.png";

    return L.icon({
        iconUrl: `/static/icons/${iconoURL}`,
        iconSize: [30, 40],
        iconAnchor: [15, 40],
        popupAnchor: [0, -35]
    });
}
