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

            mapa.setView([lat, lon], 16); // Zoom más cercano

            L.marker([lat, lon])
                .addTo(mapa)
                .bindPopup("¡Estás aquí!")
                .openPopup();
        },
        error => {
            console.error("No se pudo obtener la ubicación:", error.message);
        },
        {
            enableHighAccuracy: true, // ✅ activa máxima precisión
            timeout: 10000,
            maximumAge: 0
        }
    );
} else {
    alert("Tu navegador no soporta geolocalización.");
}


    async function mostrarTrabajadores(trabajadores) {
    markersLayer.clearLayers();
    let encontrados = 0;

    trabajadores.forEach(trab => {
        if (trab.latitud && trab.longitud) {
            const icono = trab.especialidad ? obtenerIconoPorEspecialidad(trab.especialidad.nombre_esp) : null;
            const marker = L.marker([trab.latitud, trab.longitud], icono ? { icon: icono } : undefined)
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
    "Gasfiter",
    "Electricista",
    "Carpintero",
    "Pintor",
    "Cerrajero",
    "Jardinero",
    "Albañil",
    "Técnico en refrigeración",
    "Técnico en aire acondicionado",
    "Mecánico automotriz",
    "Mecánico de bicicletas",
    "Técnico en electrodomésticos",
    "Yesero",
    "Soldador",
    "Techador",
    "Maestro de obras",
    "Instalador de pisos",
    "Instalador de ventanas y vidrios",
    "Instalador de puertas",
    "Instalador de cortinas y persianas",
    "Tapicero",
    "Herrero",
    "Paisajista",
    "Podador de árboles",
    "Mantenimiento de piscinas",
    "Personal de aseo domiciliario",
    "Personal de aseo industrial",
    "Limpieza de vidrios en altura",
    "Lavado de alfombras y tapices",
    "Flete y mudanza",
    "Chofer particular",
    "Motoboy / Delivery independiente",
    "Instalador de sistemas de riego",
    "Técnico en calefacción",
    "Técnico en paneles solares",
    "Instalador de sistemas de seguridad",
    "Instalador de antenas y TV cable",
    "Técnico en computación",
    "Desabollador y pintor automotriz"
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
        "Maestro de obras": "maestro_obras.png",
        "Instalador de pisos": "pisos.png",
        "Instalador de ventanas y vidrios": "ventanas_vidrios.png",
        "Instalador de puertas": "puertas.png",
        "Instalador de cortinas y persianas": "cortinas.png",
        "Tapicero": "tapicero.png",
        "Herrero": "herrero.png",
        "Paisajista": "paisajista.png",
        "Podador de árboles": "podador.png",
        "Mantenimiento de piscinas": "piscinas.png",
        "Personal de aseo domiciliario": "aseo_domiciliario.png",
        "Personal de aseo industrial": "aseo_industrial.png",
        "Limpieza de vidrios en altura": "limpieza_altura.png",
        "Lavado de alfombras y tapices": "alfombras.png",
        "Flete y mudanza": "flete.png",
        "Chofer particular": "chofer.png",
        "Motoboy / Delivery independiente": "motoboy.png",
        "Instalador de sistemas de riego": "riego.png",
        "Técnico en calefacción": "calefaccion.png",
        "Técnico en paneles solares": "paneles_solares.png",
        "Instalador de sistemas de seguridad": "seguridad.png",
        "Instalador de antenas y TV cable": "antenas.png",
        "Técnico en computación": "computacion.png",
        "Desabollador y pintor automotriz": "desabollador.png"
    };

    const iconoURL = iconos[nombreEspecialidad] || "default.png";

    return L.icon({
        iconUrl: `/static/icons/${iconoURL}`,
        iconSize: [30, 40],
        iconAnchor: [15, 40],
        popupAnchor: [0, -35]
    });
}
