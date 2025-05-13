document.addEventListener("DOMContentLoaded", () => {
    let mapaUbicacion;
    let markerUbicacion;

    const usuario_id = localStorage.getItem("usuario_id");
    if (!usuario_id) {
        alert("Debes iniciar sesión primero.");
        window.location.href = "/login/";
        return;
    }

    function inicializarMapaRegistro() {
        if (!mapaUbicacion) {
            mapaUbicacion = L.map("mapa-ubicacion").setView([-33.4489, -70.6693], 13);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: "© OpenStreetMap"
            }).addTo(mapaUbicacion);
        }

        setTimeout(() => {
            mapaUbicacion.invalidateSize();
        }, 300);
    }

    window.buscarDireccionEnMapa = async function () {
        const direccion = document.getElementById("direccion").value;
        if (!direccion.trim()) {
            alert("Por favor escribe una dirección.");
            return;
        }

        try {
            const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(direccion)}`);
            const data = await response.json();

            if (data && data.length > 0) {
                const lat = parseFloat(data[0].lat);
                const lon = parseFloat(data[0].lon);

                document.getElementById("latitud").value = lat;
                document.getElementById("longitud").value = lon;

                if (markerUbicacion) {
                    markerUbicacion.setLatLng([lat, lon]).openPopup();
                } else {
                    markerUbicacion = L.marker([lat, lon]).addTo(mapaUbicacion).bindPopup("Ubicación encontrada").openPopup();
                }
                mapaUbicacion.setView([lat, lon], 15);
            } else {
                alert("No se encontró la dirección.");
            }

        } catch (error) {
            console.error("Error buscando dirección:", error);
            alert("Error al buscar la dirección.");
        }
    }

    window.nextStep = function (step) {
        document.getElementById(`step-${step}`).classList.remove('active');
        document.getElementById(`step-${step + 1}`).classList.add('active');

        if (step + 1 === 4) inicializarMapaRegistro();
    }

    window.prevStep = function (step) {
        document.getElementById(`step-${step}`).classList.remove('active');
        document.getElementById(`step-${step - 1}`).classList.add('active');
    }

    document.getElementById("multiStepForm").addEventListener("submit", async function (e) {
        e.preventDefault();
        if (!document.getElementById("especialidad").value || !document.getElementById("latitud").value) {
            alert("Completa todos los campos antes de enviar.");
            return;
        }

        const formData = new FormData(this);
        formData.append("usuario", usuario_id);
        formData.append("estado_verificado", false);
        formData.append("latitud", document.getElementById("latitud").value);
        formData.append("longitud", document.getElementById("longitud").value);

        try {
            const response = await fetch("http://localhost:8000/api/trabajadores/", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();
            if (!response.ok) {
                console.error(">>> ERROR:", data);
                alert(`Error al crear el perfil: ${JSON.stringify(data)}`);
                return;
            }

            alert("Perfil creado correctamente.");
            window.location.href = "/perfil_trabajador/";
        } catch (err) {
            console.error(">>> ERROR DE CONEXIÓN:", err);
            alert("No se pudo conectar con el servidor.");
        }
    });

    async function cargarEspecialidades() {
        const select = document.getElementById("especialidad");
        try {
            const response = await fetch("http://localhost:8000/api/especialidades/");
            const especialidades = await response.json();
            select.innerHTML = '<option value="">Selecciona una especialidad</option>';
            especialidades.forEach(esp => {
                const option = document.createElement("option");
                option.value = esp.id;
                option.textContent = esp.nombre_esp;
                select.appendChild(option);
            });
        } catch (error) {
            console.error("Error cargando especialidades:", error);
            select.innerHTML = '<option value="">Error al cargar</option>';
        }
    }

    cargarEspecialidades();
});
