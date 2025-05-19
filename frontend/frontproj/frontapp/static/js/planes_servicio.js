// static/js/planes_servicio.js

document.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("planes-container");
  const servicioId = window.SERVICIO_ID;

  try {
    // 1. Traemos el servicio completo (incluye la relación 'planes')
    const res = await fetch(`http://localhost:8000/api/servicios/${servicioId}/`);
    if (!res.ok) throw new Error(res.status);
    const servicio = await res.json();

    const planes = servicio.planes || [];
    if (planes.length === 0) {
      container.innerHTML = "<p>No hay planes disponibles.</p>";
      return;
    }

    // 2. Por cada plan, creamos una tarjeta
    planes.forEach(plan => {
      const card = document.createElement("div");
      card.className = "plan-card";
      card.innerHTML = `
        <h3>${plan.nombre_plan}</h3>
        <p><strong>Precio:</strong> $${plan.precio}</p>
        <p><strong>Duración:</strong> ${plan.duracion}</p>
        <p><strong>Incluye:</strong><br>${plan.incluye.replace(/\n/g, "<br>")}</p>
        <p>${plan.descripcion_breve}</p>
      `;
      container.appendChild(card);
    });

  } catch (e) {
    console.error("Error cargando planes:", e);
    container.innerHTML = "<p>Error al cargar los planes. Intenta de nuevo más tarde.</p>";
  }
});
