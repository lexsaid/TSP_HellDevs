document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            // Evitamos que la página se recargue automáticamente
            e.preventDefault();

            // Aquí podrías agregar validaciones extra si quisieras
            console.log("Credenciales validadas. Entrando a MIZCUIN...");

            // Redireccionamos al index.html
            // Asegúrate de que la ruta sea correcta según tu estructura de carpetas
            window.location.href = "index.html";
        });
    }
});