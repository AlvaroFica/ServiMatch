document.addEventListener("DOMContentLoaded", () => {
    const mapa = L.map('mapa').setView([-33.4489, -70.6693], 13);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; CartoDB'
    }).addTo(mapa);

    let markersLayer = L.layerGroup().addTo(mapa);

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                mapa.setView([lat, lon], 14);
                L.marker([lat, lon]).addTo(mapa).bindPopup("¡Estás aquí!").openPopup();
            },
            error => console.warn("No se pudo obtener la ubicación:", error.message)
        );
    }

    async function mostrarTrabajadores(trabajadores) {
        markersLayer.clearLayers();
        let encontrados = 0;

        trabajadores.forEach(trab => {
            if (trab.latitud && trab.longitud) {
                const marker = L.marker([trab.latitud, trab.longitud])
                    .bindPopup(`
                        <strong>${trab.usuario.nombre} ${trab.usuario.apellido}</strong><br>
                        Especialidad: ${trab.especialidad ? trab.especialidad.nombre_esp : 'No definida'}
                    `);
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

    // Buscador
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

    // Sugerencias de servicios
    document.getElementById("busqueda-servicio").addEventListener("input", mostrarSugerencias);
    const lista = document.getElementById("sugerencias");

    function mostrarSugerencias() {
        const texto = document.getElementById("busqueda-servicio").value.toLowerCase().trim();
        lista.innerHTML = "";
        if (texto === "") return;

        const ejemplos = [
            "Gasfíter",
            "Electricista",
            "Carpintero",
            "Pintor",
            "Cerrajero",
            "Jardinero",
            "Albañil",
            "Técnico en refrigeración"
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

    // Manejo de barra superior con sesión (sin tocar)
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
