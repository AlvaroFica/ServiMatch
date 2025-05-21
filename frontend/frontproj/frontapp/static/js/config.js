// static/js/config.js
const API_BASE = "https://78b6-179-2-33-12.ngrok-free.app/api"; // CAMBIA AQUÍ SOLO 1 VEZ

// Ejemplo de uso en otro archivo JS:
fetch(`${API_BASE}/mercadopago/preferencia/`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ precio: 10000, descripcion: "Plan contratado" })
}).then(r => r.json()).then(data => console.log(data));
