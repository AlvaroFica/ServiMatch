    document.getElementById("form-crear-plan").addEventListener("submit", async function(e) {
      e.preventDefault();
      const form = e.target;
      const data = {
        servicio: form.servicio.value,
        nombre_plan: form.nombre_plan.value,
        precio: form.precio.value,
        duracion: form.duracion.value,
        incluye: form.incluye.value,
        descripcion_breve: form.descripcion_breve.value
      };
      try {
        const resp = await fetch("http://localhost:8000/api/planeservicio/", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify(data)
        });
        if (resp.ok) {
          document.getElementById("mensaje-exito").style.display = "block";
          setTimeout(() => {
            window.location.href = `/ver_planes_pov_trab/${form.servicio.value}/`;
          }, 1200);
        } else {
          alert("Error al crear el plan.");
        }
      } catch {
        alert("Error de conexión.");
      }
    });