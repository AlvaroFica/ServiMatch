document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const correo = document.getElementById("correo").value;
    const contraseña = document.getElementById("contraseña").value;

    fetch("http://localhost:8000/api/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ correo, contraseña })
    })
    .then(response => response.json())
    .then(data => {
        const resultado = document.getElementById("resultado");
        if (data.mensaje) {
            resultado.innerHTML = `<div class="alert alert-success">${data.mensaje}</div>`;
        } else if (data.error) {
            resultado.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        } else {
            resultado.innerHTML = `<div class="alert alert-warning">Respuesta inesperada</div>`;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("resultado").innerHTML = `<div class="alert alert-danger">Error de conexión</div>`;
    });
});