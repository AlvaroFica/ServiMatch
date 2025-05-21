async function checkTrabajador(usuarioId) {
  const r = await fetch(`http://localhost:8000/api/trabajadores/?usuario=${usuarioId}`);
  const arr = await r.json();
  return arr.length > 0;
}

document.addEventListener("DOMContentLoaded", async () => {
  const usuarioId = localStorage.getItem('usuario_id');
  const header = document.getElementById('header-tabs');
  if (!usuarioId) {
    document.querySelector('.perfil-box').innerHTML = "<p>No has iniciado sesión.</p>";
    header.innerHTML = "";
    return;
  }
  const esTrabajador = await checkTrabajador(usuarioId);

  if (esTrabajador) {
    header.innerHTML = `
      <button class="header-tab" onclick="window.location.href='/perfil_trabajador/'">TRABAJADOR</button>
      <button class="header-tab active">CLIENTE</button>
    `;
  } else {
    header.innerHTML = `
      <div class="trabajador-msg">
        <i class="fa fa-info-circle"></i> 
        <span style="margin-left:5px;">¿Te gustaría ofrecer servicios? <span style="color:#6a1bb1;font-weight:600;">Aún no eres trabajador</span></span>
      </div>
      <button class="header-tab active">CLIENTE</button>
    `;
  }
  const resp = await fetch(`http://localhost:8000/api/usuarios/${usuarioId}/`);
  const user = await resp.json();
  document.getElementById('img-perfil-cliente').src = user.foto_perfil || '/static/img/default-user.png';
  document.getElementById('nombre-cliente').innerText = user.nombre + ' ' + user.apellido;
  document.getElementById('correo-cliente').innerText = user.correo;
  document.getElementById('fecha-cliente').innerText = (user.fecha_creacion || '').substring(0,7);
  document.getElementById('direccion').innerText = 'Dirección ' + (user.comuna || '');
  document.querySelectorAll('.perfil-menu-list li').forEach(li => {
    li.onclick = () => window.location.href = li.getAttribute('data-link');
  });
});
