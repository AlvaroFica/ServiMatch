let mapaUbicacion;
let markerUbicacion;

function inicializarMapaRegistro() {
    if (!mapaUbicacion) {  // Solo inicializar una vez
        mapaUbicacion = L.map("mapa-ubicacion").setView([-33.4489, -70.6693], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: "© OpenStreetMap"
        }).addTo(mapaUbicacion);

        mapaUbicacion.on("click", function (e) {
            const { lat, lng } = e.latlng;
            document.getElementById("latitud").value = lat;
            document.getElementById("longitud").value = lng;

            if (markerUbicacion) {
                markerUbicacion.setLatLng(e.latlng);
            } else {
                markerUbicacion = L.marker(e.latlng).addTo(mapaUbicacion).bindPopup("Ubicación seleccionada").openPopup();
            }
        });
    }

    // Siempre forzar ajuste de tamaño cuando el paso 4 sea visible
    setTimeout(() => {
        mapaUbicacion.invalidateSize();
    }, 300);
}
