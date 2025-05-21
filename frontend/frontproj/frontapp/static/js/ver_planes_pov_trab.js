document.addEventListener("DOMContentLoaded", async () => {
  // Asume que tienes el ID del servicio en la URL: /ver_planes/<servicio_id>/
  const path = window.location.pathname;
  const servicioId = path.split("/").filter(Boolean).pop();
  const container = document.getElementById("planes-list");

  try {
    const resp = await fetch(`http://localhost:8000/api/planeservicio/?servicio=${servicioId}`);
    const planes = await resp.json();

    if (!planes.length) {
      container.innerHTML = "<p>No tienes planes creados aún para este servicio.</p>";
      return;
    }

    container.innerHTML = "";
    planes.forEach(plan => {
      const div = document.createElement("div");
      div.classList.add("plan-card");
      div.innerHTML = `
        <div class="plan-titulo">${plan.nombre_plan}</div>
        <div class="plan-info-row">
          <span class="plan-info-label">Precio:</span>
          <span class="plan-info-value">$${plan.precio}</span>
        </div>
        <div class="plan-info-row">
          <span class="plan-info-label">Duración:</span>
          <span class="plan-info-value">${plan.duracion} min</span>
        </div>
        <div class="plan-items">
          <span class="plan-info-label">Incluye:</span>
          <ul>
            ${(plan.items_incluidos || []).map(item => `<li>${item}</li>`).join('')}
          </ul>
        </div>
        <div class="plan-descripcion">${plan.descripcion_corta || ""}</div>
        <button class="btn-editar" onclick="location.href='/editar_plan/${plan.id}/'"><i class="fa fa-edit"></i> Editar</button>
        <button class="btn-eliminar" onclick="if(confirm('¿Eliminar plan?')) location.href='/eliminar_plan/${plan.id}/'"><i class="fa fa-trash"></i> Eliminar</button>
      `;
      container.appendChild(div);
    });
  } catch (error) {
    container.innerHTML = "<p>Error al cargar los planes.</p>";
  }
});
