document.addEventListener('DOMContentLoaded', async () => {
  const usuarioId = localStorage.getItem('usuario_id');
  if (!usuarioId) return;
  const resp = await fetch(`http://localhost:8000/api/trabajadores/?usuario=${usuarioId}`);
  const trabajadores = await resp.json();
  if (!trabajadores.length) return;
  const t = trabajadores[0];
  document.getElementById('img-perfil-trabajador').src = t.usuario.foto_perfil || '/static/img/default-user.png';
  document.getElementById('nombre-trabajador').innerText = t.usuario.nombre + ' ' + t.usuario.apellido;
  document.getElementById('especialidad-trabajador').innerText = t.especialidad?.nombre_esp || 'Sin especialidad';
  document.getElementById('fecha-trabajador').innerText = (t.usuario.fecha_creacion || '').substring(0,7);
  document.getElementById('servicios-trabajador').innerText = t.servicios?.length ?? 0;
  document.getElementById('direccion-trabajador').innerText = 'Dirección ' + (t.usuario.comuna || '');
  document.querySelectorAll('.perfil-menu-list li').forEach(li => {
    li.onclick = () => window.location.href = li.getAttribute('data-link');
  });
});
