document.addEventListener("DOMContentLoaded", async () => {
  // Obtén el id desde la URL /trabajador/123/
  const trabajadorId = window.location.pathname.split('/').filter(x => x).pop();
  const resp = await fetch(`http://localhost:8000/api/trabajadores/${trabajadorId}/`);
  if (!resp.ok) return;
  const trab = await resp.json();
  const u = trab.usuario || {};

  document.getElementById('direccion').innerText = 'Dirección ' + (u.comuna || '');
  document.getElementById('img-perfil-trab-publico').src = u.foto_perfil || '/static/img/default-user.png';
  document.getElementById('nombre-trab').innerText = (u.nombre || '') + ' ' + (u.apellido || '');
  document.getElementById('especialidad-trab').innerText = trab.especialidad?.nombre_esp || '';
  document.getElementById('antiguedad-trab').innerText = (u.fecha_creacion || '').substring(0,7);
  document.getElementById('servicios-trab').innerText = trab.servicios?.length || 0;

  let estrellas = '';
  for(let i=0; i<5; i++) {
    estrellas += i < (trab.rating || 4) ? '<i class="fa fa-star"></i> ' : '<i class="fa-regular fa-star"></i> ';
  }
  document.getElementById('estrellas-trab').innerHTML = estrellas;

  document.getElementById('btn-contratar').onclick = () => {
    if(trab.servicios && trab.servicios.length)
      window.location.href = `/planes_servicio/${trab.servicios[0].id}/`;
  };

  // Portafolio
  const grid = document.getElementById('portfolio-grid');
  if(trab.portafolio?.length) {
    trab.portafolio.forEach(img => {
      const im = document.createElement('img');
      im.src = img.url || img;
      grid.appendChild(im);
    });
  } else {
    grid.innerHTML = '<div style="color:#bbb;padding:16px 0;font-size:14px;">Este trabajador aún no ha subido portafolio.</div>';
  }

  // Evaluaciones (simuladas)
  const tags = document.getElementById('review-tags');
  (trab.evaluaciones || ['Atención a los detalles', 'Rapidez', 'Puntualidad']).forEach(txt => {
    const t = document.createElement('span');
    t.className = 'tag';
    t.innerText = txt;
    tags.appendChild(t);
  });
});
