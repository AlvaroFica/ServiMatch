;(async()=>{
  const host    = document.body.dataset.host;
  const api     = host + '/api';
  const citaId  = document.body.dataset.cita;
  const defServ = document.body.dataset.defServ;
  const defUser = document.body.dataset.defUser;
  const full    = p => p.startsWith('http') ? p : host + p;

  const cita = await fetch(`${api}/citas/${citaId}/`).then(r=>r.json());
  const plan = await fetch(`${api}/planeservicio/${cita.plan}/`).then(r=>r.json());
  const serv = await fetch(`${api}/servicios/${plan.servicio}/`).then(r=>r.json());
  const trab = await fetch(`${api}/trabajadores/${cita.trabajador}/`).then(r=>r.json());
  const usr  = trab.usuario;

  // Imagenes
  document.getElementById('img-servicio').src   =
    serv.imagenes[0]?.imagen ? full(serv.imagenes[0].imagen) : defServ;
  document.getElementById('img-trabajador').src =
    usr.foto_perfil              ? full(usr.foto_perfil)             : defUser;

  // Cabecera
  document.getElementById('nombre-servicio').textContent = serv.nombre_serv;
  document.getElementById('precio-servicio').textContent = `$${plan.precio}`;
  document.getElementById('fecha-servicio').textContent  = cita.fecha_creacion.slice(0,10);

  // Datos trabajador
  document.getElementById('nombre-trabajador').textContent  = `${usr.nombre} ${usr.apellido}`;
  document.getElementById('servicio-trabajador').textContent = serv.nombre_serv;

  // Detalles generales
  document.getElementById('asunto-detalle').textContent    = plan.descripcion_breve || '';
  document.getElementById('fecha-detalle').textContent     = cita.fecha_creacion.slice(0,10);
  document.getElementById('direccion-detalle').textContent = usr.comuna_nombre   || '';
  document.getElementById('duracion-detalle').textContent  = plan.duracion;

  // Información de pago
  const boletas = await fetch(`${api}/boletas/`).then(r=>r.json());
  const b       = boletas.find(x=>x.cita == citaId) || {};
  const monto   = b.monto || 0;
  const com     = Math.round(monto * 0.1);
  document.getElementById('precio-total').textContent      = `$${monto}`;
  document.getElementById('comision-servicio').textContent = `$${com}`;
  document.getElementById('total-recibido').textContent    = `$${monto - com}`;

  if(b.tipo_pago){
    const tp = await fetch(`${api}/tipopagos/${b.tipo_pago}/`).then(r=>r.json());
    document.getElementById('metodo-pago').textContent = tp.descripcion;
  }
  document.getElementById('estado-pago').textContent = b.id ? 'Liberado' : 'Pendiente';
})();
