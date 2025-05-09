document.addEventListener("DOMContentLoaded", () => {
    // Mostrar campo dirección si tiene valor
    const inputDireccion = document.getElementById("direccion");
    const bloque = document.getElementById("bloque-direccion");
    if (inputDireccion && inputDireccion.value.trim() !== "") {
        bloque.style.display = "block";
    }

    // Lista de servicios disponibles
    const servicios = [
        "Gasfíter",
        "Electricista",
        "Carpintero",
        "Pintor",
        "Cerrajero",
        "Jardinero",
        "Maestro albañil",
        "Técnico en refrigeración"
    ];

    // Mostrar sugerencias en tiempo real
    function mostrarSugerencias() {
        const input = document.getElementById("busqueda-servicio");
        const texto = input.value.toLowerCase().trim();
        const lista = document.getElementById("sugerencias");

        lista.innerHTML = "";
        if (texto === "") return;

        const filtrados = servicios.filter(servicio =>
            servicio.toLowerCase().includes(texto)
        );

        filtrados.forEach(servicio => {
            const item = document.createElement("li");
            item.textContent = servicio;
            item.onclick = () => {
                input.value = servicio;
                lista.innerHTML = "";
            };
            lista.appendChild(item);
        });
    }

    // Ejecutar búsqueda
    function buscarServicio() {
        const input = document.getElementById("busqueda-servicio").value;
        alert(`Buscando "${input}"...`);
        document.getElementById("sugerencias").innerHTML = "";
    }

    // Eventos del buscador
    document.getElementById("busqueda-servicio").addEventListener("input", mostrarSugerencias);
    document.getElementById("busqueda-servicio").addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            buscarServicio();
        }
    });
    document.getElementById("btn-buscar").addEventListener("click", buscarServicio);

    // ==============================
    // MAPA CON DETECCIÓN DE UBICACIÓN
    // ==============================
    const mapa = L.map('mapa').setView([-33.4489, -70.6693], 13); // Santiago por defecto

    // Capa visual
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; CartoDB'
    }).addTo(mapa);

    // Geolocalización del navegador
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                mapa.setView([lat, lon], 15);

                L.marker([lat, lon])
                    .addTo(mapa)
                    .bindPopup("¡Estás aquí!")
                    .openPopup();
            },
            error => {
                console.error("No se pudo obtener la ubicación:", error.message);
                // No hacer nada si falla, se queda en Santiago
            }
        );
    } else {
        alert("Tu navegador no soporta geolocalización.");
    }
});



function abrirOverlay() {
    document.getElementById("overlay-buscador").style.display = "flex";
    document.getElementById("busqueda-overlay").focus();
}

function cerrarOverlay() {
    document.getElementById("overlay-buscador").style.display = "none";
}

function mostrarSugerenciasOverlay() {
    const texto = document.getElementById("busqueda-overlay").value.toLowerCase().trim();
    const lista = document.getElementById("sugerencias-overlay");
    lista.innerHTML = "";

    if (texto === "") return;

    const filtrados = servicios.filter(servicio =>
        servicio.toLowerCase().includes(texto)
    );

    filtrados.forEach(servicio => {
        const item = document.createElement("li");
        item.textContent = servicio;
        item.onclick = () => {
            document.getElementById("busqueda-overlay").value = servicio;
            lista.innerHTML = "";
        };
        lista.appendChild(item);
    });
}


