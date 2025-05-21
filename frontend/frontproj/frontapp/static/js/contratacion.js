document.addEventListener("DOMContentLoaded", async () => {
  const API = 'http://localhost:8000/api';
  const planId = window.PLAN_ID;
  const usuarioId = Number(localStorage.getItem('usuario_id')) || null;

  if (!planId) {
    alert('plan_id no definido.');
    return;
  }

  let res = await fetch(`${API}/planeservicio/${planId}/`);
  if (!res.ok) {
    alert('Plan no encontrado');
    return;
  }
  const plan = await res.json();

  res = await fetch(`${API}/servicios/${plan.servicio}/`);
  if (!res.ok) {
    alert('Servicio no encontrado');
    return;
  }
  const serv = await res.json();

  document.getElementById('service-name').innerText = serv.nombre_serv;
  document.getElementById('price').innerText = `$${plan.precio}`;
  document.getElementById('service-desc').innerText = serv.descripcion_breve;
  document.getElementById('duration').innerText = plan.duracion;

  const items = plan.incluye ? plan.incluye.split('\n') : [];
  document.getElementById('jobs').innerText = `${items.length} ítems`;
  document.getElementById('includes').innerHTML = items.map(i => `<li><i class="fa fa-star"></i> ${i}</li>`).join('');

  document.getElementById('btn-contratar').addEventListener('click', async () => {
    if (!usuarioId) {
      alert('Debes iniciar sesión.');
      window.location.href = '/';
      return;
    }

    if (!serv.trabajadores || !serv.trabajadores.length) {
      alert('No hay trabajador disponible en este servicio');
      return;
    }

    const trabajadorId = serv.trabajadores[0];
    let resCita = await fetch(`${API}/citas/`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        usuario: usuarioId,
        trabajador: trabajadorId,
        plan: planId
      })
    });

    if (!resCita.ok) {
      alert('Error al crear la cita');
      return;
    }
    const cita = await resCita.json();

    let resChat = await fetch(`${API}/chats/`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        cita: cita.id,
        termino: ''
      })
    });

    if (!resChat.ok) {
      alert('Error al crear el chat');
      return;
    }
    const chat = await resChat.json();

    window.location.href = `/chat/${chat.id}/`;
  });
});
