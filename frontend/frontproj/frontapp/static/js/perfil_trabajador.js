document.addEventListener("DOMContentLoaded", async function () {
  const usuarioIdSesion = localStorage.getItem("usuario_id");

  const pathId = window.location.pathname.split("/").filter(Boolean).pop();
  const usuarioIdPerfil = isNaN(pathId) ? usuarioIdSesion : pathId;

  if (!usuarioIdPerfil) {
    alert("Sesión expirada. Iniciá sesión de nuevo.");
    window.location.href = "/login/";
    return;
  }

  try {
    const response = await fetch(`http://localhost:8000/api/trabajadores/?usuario=${usuarioIdPerfil}`);
    const data = await response.json();

    if (!data.length) {
      alert("Trabajador no encontrado.");
      return;
    }

    const trabajador = data[0];

    // Nombre y especialidad
    const nombre = `${trabajador.usuario.nombre} ${trabajador.usuario.apellido}`;
    document.getElementById("nombre-trabajador").innerText = nombre;
    document.getElementById("especialidad-trabajador").innerText =
      trabajador.especialidad?.nombre_esp || "Sin especialidad";

    // Antigüedad
    const fecha = new Date(trabajador.usuario.fecha_creacion);
    document.getElementById("fecha-creacion").innerText =
      fecha.toLocaleDateString("es-CL", { year: "numeric", month: "long" });

    // Cantidad servicios
    document.getElementById("cantidad-servicios").innerText =
      trabajador.servicios?.length || 0;

    // Foto de perfil
    if (trabajador.usuario.foto_perfil) {
      const avatar = document.getElementById("avatar");
      const img = document.createElement("img");
      img.src = trabajador.usuario.foto_perfil.startsWith("http")
        ? trabajador.usuario.foto_perfil
        : `http://localhost:8000${trabajador.usuario.foto_perfil}`;
      img.alt = "Foto de perfil";
      img.style.borderRadius = "50%";
      img.style.width = "100px";
      img.style.height = "100px";
      avatar.appendChild(img);
    }

    // Ocultar botones si el usuario visitante no es el mismo del perfil
    if (usuarioIdSesion !== usuarioIdPerfil) {
      document.querySelectorAll(".solo-propietario").forEach(el => el.style.display = "none");
    }

  } catch (error) {
    console.error("Error al cargar perfil:", error);
    alert("No se pudo cargar la información del perfil.");
  }
});
