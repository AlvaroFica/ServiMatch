async function cargarComunas() {
    try {
        const response = await fetch("http://localhost:8000/api/comunas/");
        const comunas = await response.json();
        const select = document.getElementById("comuna");
        comunas.forEach(comuna => {
            const option = document.createElement("option");
            option.value = comuna.id;
            option.textContent = comuna.nombre_comuna;
            select.appendChild(option);
        });
    } catch (error) {
        console.error("Error cargando comunas:", error);
    }
}

async function detectarUbicacion() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(async position => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            try {
                const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`);
                const data = await response.json();

                if (data && data.address) {
                    const direccion = `${data.address.road || ''} ${data.address.house_number || ''}`.trim();
                    if (direccion) document.getElementById("direccion").value = direccion;

                    const comunaNombre = data.address.suburb || data.address.city || data.address.town;
                    if (comunaNombre) {
                        const select = document.getElementById("comuna");
                        const option = Array.from(select.options).find(opt => opt.textContent.toLowerCase() === comunaNombre.toLowerCase());
                        if (option) select.value = option.value;
                    }
                }
            } catch (error) {
                console.error("Error obteniendo dirección:", error);
            }
        }, error => {
            console.warn("No se pudo obtener la ubicación:", error.message);
        });
    } else {
        console.warn("Geolocalización no soportada");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    cargarComunas().then(detectarUbicacion);

    // ✅ Formatear RUT
    document.getElementById("rut").addEventListener("input", function () {
        let valor = this.value.replace(/\./g, '').replace('-', '').replace(/[^0-9kK]/g, '').toUpperCase();
        if (valor.length > 1) {
            valor = valor.slice(0, -1) + '-' + valor.slice(-1);
        }
        valor = valor.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        this.value = valor;
    });

    // ✅ Formatear Celular (+569 y 8 dígitos)
    document.getElementById("celular").addEventListener("input", function () {
        let valor = this.value.replace(/\D/g, '');
        if (!valor.startsWith('569')) {
            valor = '569' + valor.replace(/^569/, '');
        }
        valor = '+' + valor.slice(0, 11); // +569 y 8 dígitos
        this.value = valor;
    });

    const form = document.getElementById("registro-form");
    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const pass1 = document.getElementById("contraseña").value;
        const pass2 = document.getElementById("repetir-contraseña").value;
        if (pass1 !== pass2) {
            alert("Las contraseñas no coinciden");
            return;
        }

        const correo = document.getElementById("correo").value.toLowerCase();
        const correoValido = /^[a-zA-Z0-9._%+-]+@(gmail|hotmail|outlook|yahoo|duocuc)\.(com|cl)$/.test(correo);
        if (!correoValido) {
            alert("El correo debe ser @gmail.com, @hotmail.com, @outlook.com, @yahoo.com, @duocuc.cl o @duocuc.com");
            return;
        }

        const celular = document.getElementById("celular").value;
        if (!/^\+569\d{8}$/.test(celular)) {
            alert("El celular debe ser en formato +569 seguido de 8 números (ej: +56912345678)");
            return;
        }

        const formData = new FormData(form);
        const dataUsuario = {
            rut: formData.get("rut"),
            nombre: formData.get("nombre"),
            apellido: formData.get("apellido"),
            correo: formData.get("correo"),
            telefono: formData.get("celular"),
            fecha_nac: formData.get("fecha_nacimiento"),
            comuna: formData.get("comuna"),
            direccion: formData.get("direccion"),
            contraseña: formData.get("contraseña"),
        };

        const fotoPerfil = formData.get("foto_perfil");
        const dataToSend = new FormData();
        for (let key in dataUsuario) {
            dataToSend.append(key, dataUsuario[key]);
        }
        if (fotoPerfil && fotoPerfil.size > 0) {
            dataToSend.append("foto_perfil", fotoPerfil);
        }

        try {
            const responseUsuario = await fetch("http://localhost:8000/api/usuarios/", {
                method: "POST",
                body: dataToSend,
            });

            if (!responseUsuario.ok) {
                const error = await responseUsuario.json();
                alert("Error al registrar usuario: " + JSON.stringify(error));
                return;
            }

            const usuario = await responseUsuario.json();

            const trabajadorData = {
                usuario: usuario.id,
                especialidad: null,
                estado_verificado: false
            };

            await fetch("http://localhost:8000/api/trabajadores/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(trabajadorData)
            });

            window.location.href = "/principal_pagina/";
        } catch (error) {
            console.error("Error de conexión:", error);
            alert("No se pudo conectar al servidor.");
        }
    });
});
