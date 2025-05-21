document.addEventListener("DOMContentLoaded", async () => {
  const usuarioId = localStorage.getItem("usuario_id");
  const container = document.getElementById("servicios-container");

  if (!usuarioId) {
    container.innerHTML = "<p>No has iniciado sesión.</p>";
    return;
  }

  try {
    const resp = await fetch(`http://localhost:8000/api/trabajadores/?usuario=${usuarioId}`);
    const data = await resp.json();
    if (!data.length) {
      container.innerHTML = "<p>No se encontró trabajador.</p>";
      return;
    }

    const trabajador = data[0];
    const servicios = trabajador.servicios || [];

    if (!servicios.length) {
      container.innerHTML = "<p>No tienes servicios registrados aún.</p>";
      return;
    }

    container.innerHTML = "";
    servicios.forEach(serv => {
      const div = document.createElement("div");
      div.classList.add("tarjeta-servicio");

      const imagenes = serv.imagenes?.length
        ? serv.imagenes.map(img => {
            const url = img.imagen.startsWith("http") ? img.imagen : `http://localhost:8000${img.imagen}`;
            return `<img src="${url}" alt="Imagen servicio">`;
          }).join("")
        : `<p><em>Sin imágenes</em></p>`;

      div.innerHTML = `
        <div class="encabezado-servicio">
          <strong>${serv.nombre_serv}</strong>
          <a href="/ver_planes_pov_trab/${serv.id}/" class="btn-planes">Ver planes</a>
        </div>
        <p class="descripcion">${serv.descripcion_breve || "Sin descripción."}</p>
        ${imagenes}
      `;

      container.appendChild(div);
    });

  } catch (error) {
    console.error("Error al cargar servicios:", error);
    container.innerHTML = "<p>Error al obtener tus servicios.</p>";
  }
});
